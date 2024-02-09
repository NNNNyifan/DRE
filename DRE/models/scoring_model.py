import openai
import time
import copy
from prompt.score_prompt import score_prompt
openai.api_key ="YOUR_OPENAI_KEY"


def scoring_prompt(final_recommend_exp,gpt_exp,user_review):
    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 0.95,
        "frequency_penalty": 0.4,
        "presence_penalty": 0.2, 
        'n':1
        }
    

    #得用few-shot提取
    message=score_prompt(final_recommend_exp,gpt_exp,user_review)
    return chatgpt_config,message


def score_gpt(final_recommend_exp,gpt_exp,user_review):
    response={}
    chatgpt_config,message=scoring_prompt(final_recommend_exp,gpt_exp,user_review)
    request = copy.deepcopy(chatgpt_config)
    response = openai.ChatCompletion.create( **request, messages=message)
        
    if response:
        response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]
    else:
        response = ''
    
    user_profile=response
    return user_profile


def scoring_model(final_recommend_exp,gpt_exp,user_review):

    
    def call_scoring_model():
            return score_gpt(final_recommend_exp,gpt_exp,user_review)
      
    response=call_scoring_model()
           
    return response

    
