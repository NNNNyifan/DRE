import openai
import time
import copy
openai.api_key ="YOUR_OPENAI_KEY"
from prompt.explaination_prompt import gpt_prompt
from scripts.llama_setting import chatbot2
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 

def history_item_prompt(history_item_information,rec_item_infromation):
    chatgpt_config = {"model": "gpt-3.5-turbo-16k",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }
    


    message=gpt_prompt(history_item_information,rec_item_infromation)
    return chatgpt_config,message


def chat_gpt(history_item_information,rec_item_infromation):
    response={}
    chatgpt_config,message=history_item_prompt(history_item_information,rec_item_infromation)
    request = copy.deepcopy(chatgpt_config)
    #response = openai.ChatCompletion.create( **request, messages=message)
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
            return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
    
    if response:
        response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]
    else:
        response = ''
    
    user_profile=response
    return user_profile

def call_llama2(history_item_information,rec_item_infromation):
    message=gpt_prompt(history_item_information,rec_item_infromation)
    prompt = " ".join([f"{item['role']}: {item['content']}" for item in message])
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(10))
    def completion_with_backoff(**kwargs):
        query_result = chatbot2.query(prompt)
        return query_result["text"]
    
    response=completion_with_backoff(prompt=prompt)
        
    return response

def gpt_model(history_item_information,rec_item_infromation,model):
    if model=="chat-gpt-3.5":
        def call_chatgpt():
                return chat_gpt(history_item_information,rec_item_infromation)
        
        response=call_chatgpt()
    elif model=="llama2":
        response=call_llama2(history_item_information,rec_item_infromation)
           
    return response

    
