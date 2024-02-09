import json
import threading
import torch
import numpy as np
import os
from hugchat import hugchat
from hugchat.login import Login
import sys
import tqdm
import pickle
import time
from pathlib import Path
from torch.utils.data import DataLoader
from models.LLM_chatgpt import LLM_chatgpt
from models.aspects_model import aspects_model
from models.exp_score_model import exp_score_model
from models.gpt_model import gpt_model
from models.scoring_model import scoring_model
from models.summerize_for_gpt import summerize_for_gpt
from models.user_profile_model import user_profile_model
from models.filter_model import filter_model
from scripts.preprocessing.dataset_init import dataset_init
from utils.argument_amazon import arg_parse_train_base, arg_parser_preprocessing
from models.data_loaders import UserItemInterDataset
from models.models import BaseRecModel
from utils.evaluate_functions import compute_ndcg
from scripts.explain_model import explain_model
from models.rec_history_data_process import All_rec_history_data_process
from hugchat import hugchat
from hugchat.login import Login


review_num_test="./Ablation_output/history_test/Home_3_2.json"
file_test="Phone_information.json"
        
def train_base_recommendation(train_args, pre_processing_args):
    if train_args.gpu:
        device = torch.device('cuda:%s' % train_args.cuda)
    else:
        device = 'cpu'
    
    model=pre_processing_args.llm_model
    review_num=pre_processing_args.review_num
        
    rec_dataset = dataset_init(pre_processing_args)
    Path(pre_processing_args.save_path).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(pre_processing_args.save_path, pre_processing_args.dataset + "_dataset_obj.pickle"), 'wb') as outp:
        pickle.dump(rec_dataset, outp, pickle.HIGHEST_PROTOCOL)
    

    users=rec_dataset.users    
    begin_user=0
    count=begin_user
    num=begin_user
    
    users=users[begin_user:]
    for user_key in users:
          
          num+=1
          rec_item_infromation,history_item_information,user_review_on_rec,history_item_review,rec_item_other_user_review,user_history_review=All_rec_history_data_process(user_key,rec_dataset,review_num)
          
          count+=1
          if count==16: break
           
          information={
            "recommended item":rec_item_infromation,
            "history item":history_item_information
          }
          with open(item_information,'a') as f:
            json.dump(information,f)
            f.write("\n,")
          continue
          
          summeraize_rec_information=LLM_chatgpt(rec_item_infromation,rec_item_other_user_review,model)
          print("user summerize finnished")
          
          user_aspects=aspects_model(user_review_on_rec,model)
          # print("user aspects finished")
          
          for i in range(1):
            final_recommend_exp,filter_score,user_profile,filter_history_information=explain_model(rec_item_infromation,history_item_information,user_review_on_rec,history_item_review,user_aspects,summeraize_rec_information,user_history_review,model)
              
          print(f"finished {count}")  
          
          continue

          summerize_len=len(history_item_information)
          threads=[]
          summerize_item_information_review={}
          for i in range(summerize_len):
            item_information=list(history_item_information.values())[i]
            key = list(history_item_review.keys())[i]
            item_review=history_item_review[key]
            summerize_item_information_review[i]={
              'description':item_information,
              'other_users_reviews':item_review
            }
            thread = threading.Thread(target=summerize_for_gpt, args=(i,item_information,item_review,summerize_item_information_review,model))
            threads.append(thread)
            thread.start()
          
          for thread in threads:
              thread.join()
          print("summerize has finished")  
          
        
          
          #-----------------Compare with gpt-------------------------------------------------------
          gpt_exp=gpt_model(summerize_item_information_review,rec_item_infromation,model)
          
          gpt_score=exp_score_model(Mixtral_exp,user_aspects)
          print("score has finished")
          

          print(f"finished{count}")
          
          try:
                gpt_score=int(gpt_score)
          except ValueError:
                gpt_score=gpt_score
                
          try:
                filter_score=int(filter_score)
          except ValueError:
                filter_score=filter_score                  
            
          try:
              filter_int=int(filter_score)
              gpt_int=int(gpt_score)
              if filter_int > gpt_int:
                  ans = 1  # filter的回答是1，gpt的回答是2
              elif filter_int < gpt_int:
                  ans = 2
              else:
                  ans = 0
          except ValueError:
                  ans=None
                  
          result={
              'ans':ans,
              'matrix filter_score':filter_score,
              'matrix gpt_score':gpt_score,
              'matrix filter response':final_recommend_exp,
              'matrix gpt response':gpt_exp
            }
          with open('./output/matrix/Phone_and_Acc_2.json', 'a') as file_out:
            json.dump(result,file_out)
            file_out.write(",\n")
          #------------------------------------------------------------------------
          print(f"finished{count}")                
          
          
          
  

        
        
    return 0


if __name__ == "__main__":
    torch.manual_seed(0)
    np.random.seed(0)
    t_args = arg_parse_train_base()  # training arguments
    p_args = arg_parser_preprocessing()  # pre processing arguments
    if t_args.gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = t_args.cuda
        print("Using CUDA", t_args.cuda)
    else:
        print("Using CPU")
    print(p_args)
    train_base_recommendation(t_args, p_args)  