import openai
import copy
from prompt.history_movie_profile import history_movie_profile
from prompt.single_history_movie_profile import llama_single_history_profile, single_history_movie_profile
from scripts.llama_setting import chatbot

openai.api_key ="YOUR_OPENAI_KEY"
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 


# def history_item_prompt(item_description,item_review,summeraize_rec_information):
#     chatgpt_config = {"model": "gpt-3.5-turbo",
#         "temperature": 1,
#         "max_tokens": 1024,
#         'n':1
#         }
    
#     message=single_history_movie_profile(item_description,item_review,summeraize_rec_information)
#     return chatgpt_config,message


def chat_gpt(item_description,item_review,summeraize_rec_information):
    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }
    
    message=single_history_movie_profile(item_description,item_review,summeraize_rec_information)
    
    #chatgpt_config,message=history_item_prompt(item_description,item_review,summeraize_rec_information)
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

def llama_filter(item_description,item_review,summeraize_rec_information):
    
    prompt=llama_single_history_profile(item_description,item_review,summeraize_rec_information)
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
        query_result = chatbot.query(prompt)
        return query_result["text"]
    
    response=completion_with_backoff(prompt=prompt)
    
    return response
    
def filter_model(idex,item_description,item_review,summeraize_rec_information,filter_history_information,model):
    
    if model=="chat-gpt-3.5":    
      history_profile =chat_gpt(item_description,item_review,summeraize_rec_information)
    elif model=="llama2":
      history_profile =llama_filter(item_description,item_review,summeraize_rec_information)  
      
    filter_history_information[idex]=history_profile
    

    #return history_profile
