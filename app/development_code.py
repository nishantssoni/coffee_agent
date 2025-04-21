from agents import (GuardAgent,
                    ClassificationAgent,
                    DetailsAgent,
                    RecommendationAgent,
                    OrderTakingAgent
                    )
from agents import AgentProtocol
import os

def main():
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    recommendation_agent = RecommendationAgent("python_code/api/recommendation_objects/apriori_recommendation.json","python_code/api/recommendation_objects/popularity_recommendation.csv")
    
    agent_dict: dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "order_taking_agent": OrderTakingAgent(recommendation_agent),
        "recommendation_agent": recommendation_agent
    }

    messages = []

    # recommendation_agent = RecommendationAgent()
    # print(recommendation_agent.get_apriori_recommendation(['Croissant']))
    while True:
        # Display the chat history
        # os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\nPrint Messages ...............")
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")

        # Get user input
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})

    
        # Get Guard agent response
        response = guard_agent.get_response(messages)
        # print("Guard: ", response)
        if response["memory"]["guard_decision"] == "not allowed":
            messages.append(response)
            continue

        # Get classification agent
        response = classification_agent.get_response(messages)
        chosen_agent = response["memory"]["classification_decision"]

        # get the chosen agent's response
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        messages.append(response)
        print(response)


if __name__ == "__main__":
    main()

