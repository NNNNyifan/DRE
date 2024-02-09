import openai
import copy
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from prompt.history_movie_profile import history_movie_profile
from prompt.single_history_movie_profile import single_history_movie_profile
openai.api_key ="YOUR_OPENAI_KEY"

system="""
you are an emotional judgment assistant,Determine whether the review of the film is positive or negative.
if review is positive, response: '1'
if review is negative, response:'-1'

you can only response '1' or '-1', can't use any other words.

"""


def judge(review):

    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 0.95,
        "frequency_penalty": 0.4,
        "presence_penalty": 0.2, 
        'n':1
        }
    
    message=[]
    query=f"this is review:{review}"
    message.append({"role": "system", "content": system})
    message.append({"role": "user","content":query})
    
    request = copy.deepcopy(chatgpt_config)
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
         return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
    #response = openai.ChatCompletion.create( **request, messages=message)
        
    if response:#response里有多个回答，选择第0个作为本次对话的实际对话
        response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]
    else:
        response = ''
    
    
    return response


def Emotional_judgement(review):
    

    emotion =judge(review)

    

    return emotion