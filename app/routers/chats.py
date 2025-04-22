from fastapi import FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Optional
# At the top of your routers/user.py:
import sys
from pathlib import Path
import ast
from sqlalchemy import desc

# This line gets the absolute path to your root directory
ROOT_DIR = Path(__file__).parent.parent  # Goes up one level from 'routers'
sys.path.insert(0, str(ROOT_DIR))
import schemas
import models
from database import engine, get_db
import oauth2
from agents import AgentProtocol
from agents import (GuardAgent,
                    ClassificationAgent,
                    DetailsAgent,
                    RecommendationAgent,
                    OrderTakingAgent
                    )
guard_agent = GuardAgent()
classification_agent = ClassificationAgent()
recommendation_agent = RecommendationAgent("./recommendation_objects/apriori_recommendation.json","./recommendation_objects/popularity_recommendation.csv")
agent_dict: dict[str, AgentProtocol] = {
    "details_agent": DetailsAgent(),
    "order_taking_agent": OrderTakingAgent(recommendation_agent),
    "recommendation_agent": recommendation_agent
}


router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

@router.post("/ask", status_code=status.HTTP_201_CREATED, response_model=schemas.ChatResponse)
async def ask_model( data: schemas.PromptRequest,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # save the user prompt in the db
    db_chat = models.Chats(
                    user_id=current_user.id,
                    role="user",
                    content=data.prompt,
                    memory={},
                )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    # fetch the previous messages
    last_chats = (
        db.query(models.Chats)
        .filter(models.Chats.user_id == current_user.id)
        .order_by(desc(models.Chats.created_at))
        .all()
    )

    # format the last three messages
    formatted_chats = []
    for chat in reversed(last_chats):  # Reverse to maintain chronological order
        formatted_chats.append({"role": chat.role, "content": chat.content, "memory": chat.memory})
    
    # print("\n\n\nformatted chats : ",formatted_chats)

    # added the user prompt with the last three messages
    prompt = [{"role": "user", "content": data.prompt}] + formatted_chats

    # Get Guard agent response
    response = guard_agent.get_response(prompt)
    if response["memory"]["guard_decision"] == "allowed":
        # Get classification agent
        response = classification_agent.get_response(prompt)
        chosen_agent = response["memory"]["classification_decision"]

        # get the chosen agent's response
        agent = agent_dict[chosen_agent]
        response = agent.get_response(prompt)

    # parse the response
    parsed_response = None

    if isinstance(response, dict):
        if "message" in response and isinstance(response["message"], str):
            try:
                parsed_response = ast.literal_eval(response["message"])
            except (SyntaxError, ValueError):
                print(f"Error: Could not parse response message: {response['message']}")
                return {"error": "Invalid response format from guard agent (message)"}
        else:
            # if response is already dictionary
            parsed_response = response

        if isinstance(parsed_response, dict):
            role = parsed_response.get("role")
            content = parsed_response.get("content")
            memory = parsed_response.get("memory")

            if role and content is not None: # content can be an empty string but not None
                db_chat = models.Chats(
                    user_id=current_user.id,
                    role=role,
                    content=content,
                    memory=memory
                )
                db.add(db_chat)
                db.commit()
                db.refresh(db_chat)
                return db_chat
            else:
                print(f"Error: 'role' or 'content' missing in parsed response: {parsed_response}")
                return {"error": "Invalid response from guard agent (missing fields)"}
        else:
            print(f"Error: Parsed response is not a dictionary: {parsed_response}")
            return {"error": "Invalid response format from guard agent (parsed)"}
    else:
        print(f"Error: Unexpected response format from guard agent: {response}")
        return {"error": "Unexpected response from guard agent (overall)"}

    return {"error": "Failed to process the guard agent's response"}


@router.get("/history", response_model=List[schemas.ChatHistory])
async def get_chat_history(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    """Retrieves the chat history for the current user."""
    chats = db.query(models.Chats).filter(models.Chats.user_id == current_user.id).order_by(models.Chats.created_at).all()
    return chats