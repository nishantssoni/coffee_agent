from openai import OpenAI
# from sentence_transformers import SentenceTransformer
# from huggingface_hub import snapshot_download
# import faiss
import numpy as np
from dotenv import load_dotenv
load_dotenv()


def get_chat_response(client, model_name, messages, temprature=0.0, top_p=0.8, max_tokens=5000):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=temprature,
        top_p=top_p,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content


def get_embedding(model,text_input):
    embedding = model.encode([text_input], normalize_embeddings=True)
    embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    return embedding


def double_check_json_output(client,model_name,json_string):
    prompt = f"""
            You are a JSON validator and fixer.

            You will be given an input that is **supposed** to be a single, valid JSON object, but it may contain:
            - Multiple JSON objects (one after another without being in an array)
            - Syntax errors (missing commas, quotes, or brackets)
            - Use of single quotes instead of double quotes
            - Non-string values (convert all values to strings)
            - Escaped characters or malformed JSON

            Your job:
            - If the input is a valid **single** JSON object, return it exactly as it is.
            - If the input contains **multiple** JSON objects, only return the **first valid object**.
            - If the input is invalid, return a **corrected single valid JSON object** based on the content.
            - DO NOT return anything except a valid JSON object.
            - DO NOT return arrays, explanations, or any extra content — just one valid JSON object.

            Here is the input:
            {json_string}
        You are not allowed to return anything other than a valid JSON object.and also dont write anything other that json object
        before or after curly brackets of the json object.
"""

    messages = [{"role": "user", "content": prompt}]

    response = get_chat_response(client,model_name,messages)

    return response