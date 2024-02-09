import openai
import copy
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from prompt.history_movie_profile import history_movie_profile
from prompt.single_history_movie_profile import single_history_movie_profile
from scripts.llama_setting import chatbot2
openai.api_key ="YOUR_OPENAI_KEY"

system="""
you are a summerize assistant,summerize each item information,response strictly as follows:
item:{item name}
description:{item description}
other users' review: {other users' reviews}

each description have to under 100 words,each review have to under 100 words

"""


def summerize(history_item_review,history_item_information):

    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 1024,
        'n':1
        }
    
    message=[]
    query=f"this is review:{history_item_review},this is information{history_item_information}"
    message.append({"role": "system", "content": system})
    message.append({"role": "user","content":query})
    
    request = copy.deepcopy(chatgpt_config)
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
         return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
    #response = openai.ChatCompletion.create( **request, messages=message)
        
    if response:
        response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]
    else:
        response = ''
    
    
    return response

def llama_summerize(user_his_review,information):
    prompt=f"""
        you are a summerize assistant,summerize each item information,response strictly as follows:
        item:[item name] other user's review:[item review]
        each description have to under 50 words,each review have to under 50 words
        
        key information: item information {information},review:{user_his_review}
        """

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
        query_result = chatbot2.query(prompt)
        return query_result["text"]
    
    response=completion_with_backoff(prompt=prompt)
        
    return response
        

def summerize_for_gpt(index,history_item_information,history_item_review,summerize_item_information_review,model):
    
    if model=="chat-gpt-3.5":
       sumerize_information =summerize(history_item_review,history_item_information)
       
    elif model=="llama2":
       sumerize_information =llama_summerize(history_item_review,history_item_information)
    
    summerize_item_information_review[index]=sumerize_information
       

    
    #return sumerize_information

def summerize_for_filter(i,user_his_review,user_history_reviews,model):
    information=""
    if model=="chat-gpt-3.5":
      sum=summerize(user_his_review,information)
    elif model=="llama2":
      sum=llama_summerize(user_his_review,information)
          
    user_history_reviews[i]=sum
    
    #return sum