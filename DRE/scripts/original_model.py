import json
import threading
import torch
import numpy as np
import os
from hugchat import hugchat
from hugchat.login import Login
from models.gpt_non_history_model import gpt_non_history_model
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
from scripts.preprocessing.dataset_init import dataset_init
from utils.argument_amazon import arg_parse_train_base, arg_parser_preprocessing
from models.data_loaders import UserItemInterDataset
from models.models import BaseRecModel
from utils.evaluate_functions import compute_ndcg
from scripts.explain_model import explain_model
from models.rec_history_data_process import All_rec_history_data_process
from hugchat import hugchat
from hugchat.login import Login



# ours_dir="./Ablation_output/Ablation_response/Abation_user_profile_Cloth_remove.json"
# ablation_all_dir="./output/gpt_four_input/gpt_Cloth.json"

# compare_response="./Ablation_output/Ablation_response/compare_cloth.json"

ablation_only_target="./Ablation_output/only_target/Home_new.json"

def train_base_recommendation(train_args, pre_processing_args):
    if train_args.gpu:
        device = torch.device('cuda:%s' % train_args.cuda)
    else:
        device = 'cpu'
    
    model=pre_processing_args.llm_model
        
    rec_dataset = dataset_init(pre_processing_args)
    Path(pre_processing_args.save_path).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(pre_processing_args.save_path, pre_processing_args.dataset + "_dataset_obj.pickle"), 'wb') as outp:
        pickle.dump(rec_dataset, outp, pickle.HIGHEST_PROTOCOL)
    

    
    review_num=pre_processing_args.review_num
    begin_user=0
    count=begin_user
    num=begin_user
    users=rec_dataset.users
    users=users[begin_user:]
    for user_key in users:
          
          num+=1
          
          count+=1
          if count==101: break
          rec_item_infromation,history_item_information,user_review_on_rec,history_item_review,rec_item_other_user_review,user_history_review=All_rec_history_data_process(user_key,rec_dataset,review_num)
          
          user_aspects=aspects_model(user_review_on_rec,model)
          exp=gpt_non_history_model(rec_item_infromation)
          score=exp_score_model(exp,user_aspects)
         
          result={
              "score":score,
              "response":exp
          }  
          with open(ablation_only_target,"a") as file:
              json.dump(result,file)
              file.write(",\n")
              
            
          
       
          
          

        
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