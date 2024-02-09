import openai
import copy
from scripts.llama_setting import chatbot
from prompt.aspects_prompt import aspects_prompt
from prompt.aspects_prompt import llama_aspects_prompt
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 

def aspects_model(user_review,model):
    model="chat-gpt-3.5"
    if model=="chat-gpt-3.5":
        chatgpt_config = {"model": "gpt-3.5-turbo",
            "temperature": 1,
            "max_tokens": 1024,
            'n':1
            }

        #得用few-shot提取
        message=aspects_prompt(user_review)
        
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
            
    elif model=="llama2":
        prompt=llama_aspects_prompt(user_review)
        @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
        def completion_with_backoff(**kwargs):
                query_result = chatbot.query(prompt)
                return query_result["text"]
        
        
        response=completion_with_backoff(prompt=prompt)
 
    
    return response