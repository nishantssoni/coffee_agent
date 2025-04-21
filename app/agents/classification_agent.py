from openai import OpenAI
import os
from copy import deepcopy
from .utils import get_chat_response, double_check_json_output
import json
from config import settings


class ClassificationAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.TOKEN,
            base_url=settings.BASE_URL,
        )
        self.model_name = settings.MODEL_NAME
    
    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for a coffee shop application.
            Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
            1. details_agent: This agent is responsible for answering questions about the coffee shop, like location, delivery places, working hours, details about menue items. Or listing items in the menu items. Or by asking what we have.
            2. order_taking_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the order untill it's complete.
            3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for a recommendation, this agent should be used.

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": "go over each of the agents above and write some your thoughts about what agent is this input relevant to.",
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those. and only write the word.,
            "message": "leave the message empty.",
            }

            Your not allowed to return anything other than a valid JSON object.
        """
        input_messages = [{"role": "system", "content": system_prompt}]  + messages[-3:]

        chatbot_response = get_chat_response(self.client, self.model_name, input_messages,max_tokens=1000)
        output = self.postprocess(chatbot_response)

        return output
    
    def postprocess(self, response):
        print("the classification agent response : ",response)
        try:
            output = json.loads(response)
        except:
            corrected_json = double_check_json_output(self.client,self.model_name,response)
            output = json.loads(corrected_json)
            
        dict_output = {
        "role": "assistant",
        "content": output["message"],
        "memory":{
            "agent":"classification_agent",
            "classification_decision":output["decision"],
                }
        }

        return dict_output