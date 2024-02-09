import openai
import copy
import time
from prompt.exp_score_prompt import exp_score_prompt, llama_exp_score_prompt 
from scripts.llama_setting import chatbot
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 

openai.api_key ="YOUR_OPENAI_KEY"

def exp_setting(final_recommend_exp,user_aspects):
    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 1024,
        'n':1
        }

    #得用few-shot提取
    message=exp_score_prompt(final_recommend_exp,user_aspects)
    return chatgpt_config,message


def exp_score(final_recommend_exp,user_aspects):
    chatgpt_config,message=exp_setting(final_recommend_exp,user_aspects)
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
    

    return response

def llama_exp_score(final_recommend_exp,user_aspects):
    prompt=llama_exp_score_prompt(final_recommend_exp,user_aspects)
    #query_result=chatbot.query(prompt,retry_count=20)
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
        query_result = chatbot.query(prompt)
        return query_result["text"]
    
    response=completion_with_backoff(prompt=prompt)
    
    return response

def exp_score_model(final_recommend_exp,user_aspects):
    

    response=exp_score(final_recommend_exp,user_aspects)
    # elif model=="llama2":
    #    response=llama_exp_score(final_recommend_exp,user_aspects)
       
    return response


