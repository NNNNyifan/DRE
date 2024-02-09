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



def gpt_non_history_model(rec_item_infromation):
    chatgpt_config = {"model": "gpt-3.5-turbo",
            "temperature": 1,
            "max_tokens": 1024,
            'n':1
            }


    message=[]
    system="you are a recommend system assistant"
    user=f"Explain in precise and concise terms why you recommend this item {rec_item_infromation}"
        
    message.append({"role":"user","content":system})
    message.append({"role":"user","content":user})
        
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
