import openai
import time
import copy
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 
from prompt.user_profile_prompt import user_profile_llama_prompt, user_profile_prompt
from scripts.llama_setting import chatbot
openai.api_key ="YOUR_OPENAI_KEY"


def user_profile_setting(user_history_review,rec_item_infromation):
    chatgpt_config = {
        "model": "gpt-3.5-turbo-16k",
        "temperature": 0,
        "max_tokens": 1024,
        'n':1
        }
    
    message=user_profile_prompt(user_history_review,rec_item_infromation)
    return chatgpt_config,message


def user_profile_gpt(user_history_review,rec_item_infromation):
    response={}
    chatgpt_config,message=user_profile_setting(user_history_review,rec_item_infromation)
    request = copy.deepcopy(chatgpt_config)
    #response = openai.ChatCompletion.create( **request, messages=message)
    max_tokens=4097
    
    #if(len(message)>max_tokens): message[1]['content']=message[:max_tokens]
    
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

def user_profile_llama(user_history_review,rec_item_infromation):
    prompt=user_profile_llama_prompt(user_history_review,rec_item_infromation)
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
        query_result = chatbot.query(prompt)
        return query_result["text"]
    
    response=completion_with_backoff(prompt=prompt)
    return response
       
def user_profile_model(user_history_review,rec_item_infromation,model):
    if model=="chat-gpt-3.5":
      response=user_profile_gpt(user_history_review,rec_item_infromation)
    elif model=="llama2":
      response=user_profile_llama(user_history_review,rec_item_infromation)       
    return response

    
