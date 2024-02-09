from aiohttp import ClientSession
import openai
import copy
from prompt.recommend_item_profile_prompt import llama_prompt, recommend_item_profile_prompt
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 
openai.api_key ="YOUR_OPENAI_KEY"
from hugchat import hugchat
from hugchat.login import Login
from scripts.llama_setting import chatbot

def chat_gpt(rec_item_information,rec_item_other_user_review):
        
        chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }
        
       
        request = copy.deepcopy(chatgpt_config)
        message= recommend_item_profile_prompt(rec_item_information,rec_item_other_user_review)
   
        #response = openai.ChatCompletion.create( **request, messages=message)
        
        @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
        def completion_with_backoff(**kwargs):
                return openai.ChatCompletion.create(**kwargs)
    
    
        response=completion_with_backoff(**request, messages=message)

        if response:
            response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]
        else:
            response = ''
        return response
        
def llama_profile(rec_item_information,rec_item_other_user_review):
    
    prompt=llama_prompt(rec_item_information,rec_item_other_user_review)
    #query_result = chatbot.query(prompt)
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
        query_result = chatbot.query(prompt)
        return query_result["text"]
    
    response=completion_with_backoff(prompt=prompt)
        
    return response

def LLM_chatgpt(rec_item_information,rec_item_other_user_review,model):
    
    if model=="chat-gpt-3.5":
      item_profile=chat_gpt(rec_item_information,rec_item_other_user_review)#使用大语言模型
    elif model=="llama2":
      item_profile=llama_profile(rec_item_information,rec_item_other_user_review)
    
    return item_profile



