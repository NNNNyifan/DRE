import openai
import copy
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 

def GPT_label(USER_HISTORY,ITEM):
    user=f"""
    now you are an recommend system assistant, Considering user: {USER_HISTORY} and item: {ITEM} , will the user like the item?"
    
    you can only response : YES/NO.
    """
    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }
    request = copy.deepcopy(chatgpt_config)
    message=[]
    message.append({"role":"user","content":user})
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
            return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
    response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]

    
    return response

def Get_item_discrimination(ITEM):
    user=f"""
    Can you tell me the 'TITLE/DESCRIPTION/TAGS/SIMILAR ITEM TITLE/BRAND/FEATURE' of the item: {ITEM} ?
    you have to response in this formate:'TITLE/DESCRIPTION/TAGS/SIMILAR ITEM TITLE/BRAND/FEATURE'
    """
    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }
    request = copy.deepcopy(chatgpt_config)
    message=[]
    message.append({"role":"user","content":user})
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
            return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
    response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]

    
    return response

def Get_reconstruct_title(history_item_discrimination):
    user=f"""
    Given the user purchase history: {history_item_discrimination} , generate his history titles.
    """
    chatgpt_config = {"model": "gpt-3.5-turbo-16k",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }
    request = copy.deepcopy(chatgpt_config)
    message=[]
    message.append({"role":"user","content":user})
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
            return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
    response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]

    
    return response

def get_explanation(recommend_item_label,rec_item_discrimination,history_item_discrimination):
    user=f"""
    The user has the following purchase history: {history_item_discrimination} . Will the user like the item: {rec_item_discrimination} ?\
    Please give your answer and explain why you make this decision from the perspective of a recommendation model. \
    Your explanation should include the following aspects: summary of patterns and traits from user purchase history, the consistency or inconsistency between user preferences and the item.
    """
    chatgpt_config = {"model": "gpt-3.5-turbo-16k",
        "temperature": 1,
        "max_tokens": 1024,
        'n':1
        }
    request = copy.deepcopy(chatgpt_config)
    message=[]
    message.append({"role":"user","content":user})
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
            return openai.ChatCompletion.create(**kwargs)
    
    
    response=completion_with_backoff(**request, messages=message)
    response = response['choices'][0]['message']['content'] #[response['choices'][i]['text'] for i in range(len(response['choices']))]
    
    return response


def Interest_classification(history_item_title,recommend_item_title):
    
    label=GPT_label(history_item_title,recommend_item_title)
    return label


def Item_discrimination(item):
    item_information=Get_item_discrimination(item)
    return item_information


def History_reconstruction(history_item_discrimination):
    reconstruct_title=Get_reconstruct_title(history_item_discrimination)
    return reconstruct_title

def Rec_explanation(recommend_item_label,rec_item_discrimination,history_item_discrimination):
    explanation=get_explanation(recommend_item_label,rec_item_discrimination,history_item_discrimination)
    return explanation