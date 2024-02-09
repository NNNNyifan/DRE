import json
import threading
from models.LLM_chatgpt import LLM_chatgpt
from models.aspects_model import aspects_model
from models.exp_score_model import exp_score_model
from models.filter_model import filter_model
from models.exp_model import exp_model
from models.gpt_model import gpt_model
from models.scoring_model import scoring_model
from models.summerize_for_gpt import summerize_for_filter, summerize_for_gpt
from models.user_profile_model import user_profile_model



def explain_model(rec_item_infromation,history_item_information,user_review_on_rec,history_item_review,user_aspects,summeraize_rec_information,user_history_review,model):
    
                
    num_threads=len(history_item_information)
    threads = []
    filter_history_information={}
    for i in range(num_threads):
        item_description=list(history_item_information.values())[i]
        item_review=list(history_item_review.values())[i]
        thread = threading.Thread(target=filter_model, args=(i,item_description,item_review,summeraize_rec_information,filter_history_information,model))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()
    
    print("history filter finished")
    #------------------------------------------------------------

    
    final_recommend_exp,query=exp_model(filter_history_information,summeraize_rec_information,user_profile,model)
    print("final recommend has finished")
    
    
    filter_score=exp_score_model(final_recommend_exp,user_aspects)

    return final_recommend_exp,filter_score,user_profile,filter_history_information