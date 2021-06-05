# Major part of this code is taken from https://huggingface.co/blog/few-shot-learning-gpt-neo-and-inference-api

import json
import requests


API_TOKEN = ""

def query(payload='',parameters=None,options={'use_cache': False}):
    API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    body = {"inputs":payload,'parameters':parameters,'options':options}
    response = requests.request("POST", API_URL, headers=headers, data= json.dumps(body))
    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError:
        return "Error:"+" ".join(response.json()['error'])
    else:
      return response.json()[0]['generated_text']

parameters = {
    'max_new_tokens':25,  # number of generated tokens
    'temperature': 0.5,   # controlling the randomness of generations
    'end_sequence': "###" # stopping sequence for generation
}

girdi="""
Convert text to Python 3 code: 

Text: Create a list and add 3 to it
Code: 
a = list()
a.append(3)
###
Text: Print "hello world"
Code: 
a = "hello world"
print(a)
###
Text: Add 5 to list
Code: 
a.append(5)
###
Text: Create a dictionary
Code:
a = dict()
###
Text: Import OpenCV
Code: 
import cv2
###
Text: Get user age and add it to a dictionary
Code: 
"""            

data = query(girdi, parameters)

print(data)
