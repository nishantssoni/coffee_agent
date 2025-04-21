from openai import OpenAI
import os
from copy import deepcopy
from .utils import get_chat_response, double_check_json_output
from dotenv import load_dotenv
from config import settings
import json


class GuardAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.TOKEN,
            base_url=settings.BASE_URL,
        )
        self.model_name = settings.MODEL_NAME
    
    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine whether the user is asking something relevant to the coffee shop or not.
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menue items and coffee shop related questions.
            2. Ask questions about menue items, they can ask for ingredients in an item and more details about the item.
            3. Make an order.
            4. ASk about recommendations of what to buy.

            The user is NOT allowed to:
            1. Ask questions about anything else other than our coffee shop.
            2. Ask questions about the staff or how to make a certain menue item.

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": go over each of the points above and make see if the message lies under this point or not. Then you write some your thoughts about what point is this input relevant to.
            "decision": "allowed" or "not allowed". Pick one of those. and only write the word.
            "message": leave the message empty if it's allowed, otherwise write "Sorry, I can't help with that. Can I help you with your order?"
            }
            make sure to include each field in the output.
            """

        input_messages = [{"role": "system", "content": system_prompt}]  + messages[-3:]

        chatbot_response = get_chat_response(self.client, self.model_name, input_messages,max_tokens=1000)
        output = self.postprocess(chatbot_response)

        return output
    
    def postprocess(self, response):
        print("the gaurd agent response : ",response)
        try:
            output = json.loads(response)
        except:
            corrected_json = double_check_json_output(self.client,self.model_name,response)
            output = json.loads(corrected_json)
        
        dict_output = {
            "role": "assistant",
            "content": output["message"],
            "memory":{
                "agent":"gurad_agent",
                "guard_decision":output["decision"],
            }
        }

        return dict_output