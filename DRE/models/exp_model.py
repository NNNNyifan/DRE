import openai
import copy
import time 
from scripts.llama_setting import chatbot
from prompt.explaination_prompt import explaination_prompt
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 

openai.api_key ="YOUR_OPENAI_KEY"

def exp_setting(filter_history_information,summeraize_rec_information,user_profile):
    chatgpt_config = {"model": "gpt-3.5-turbo-16k",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }

    #得用few-shot提取
    query,message=explaination_prompt(filter_history_information,summeraize_rec_information,user_profile)
    return chatgpt_config,message,query


def exp_gpt(filter_history_information,summeraize_rec_information,user_profile):
    chatgpt_config,message,query=exp_setting(filter_history_information,summeraize_rec_information,user_profile)
    request = copy.deepcopy(chatgpt_config)
    #response = openai.ChatCompletion.create( **request, messages=message)
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
            return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
        
    if response:#response里有多个回答，选择第0个作为本次对话的实际对话
        response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]
    else:
        response = ''
    
    return response,query

def llama_gpt(filter_history_information,summeraize_rec_information,user_profile):
    prompt=exp_setting
    query,message=explaination_prompt(filter_history_information,summeraize_rec_information,user_profile)
    prompt=" ".join([f"{item['role']}: {item['content']}" for item in message])
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
        query_result = chatbot.query(prompt)
        return query_result["text"]
    
    response=completion_with_backoff(prompt=prompt)
    
    return response

def exp_model(filter_history_information,summeraize_rec_information,user_profile,model):
    query=""
    if model=="chat-gpt-3.5":
      response,query=exp_gpt(filter_history_information,summeraize_rec_information,user_profile)
    elif model=="llama2":
      response=llama_gpt(filter_history_information,summeraize_rec_information,user_profile)
    return response,query


