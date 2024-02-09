import json
import threading
import torch
import numpy as np
import os
import sys
from RecExplainer_function import History_reconstruction, Interest_classification, Item_discrimination, Rec_explanation
from models.aspects_model import aspects_model
from models.exp_score_model import exp_score_model
import pickle
from pathlib import Path
from scripts.preprocessing.dataset_init import dataset_init
from utils.argument_amazon import arg_parse_train_base, arg_parser_preprocessing
from models.rec_history_data_process import All_rec_history_data_process, get_history_item_title


def train_base_recommendation(train_args, pre_processing_args):
    if train_args.gpu:
        device = torch.device('cuda:%s' % train_args.cuda)
    else:
        device = 'cpu'

        
    rec_dataset = dataset_init(pre_processing_args)
    Path(pre_processing_args.save_path).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(pre_processing_args.save_path, pre_processing_args.dataset + "_dataset_obj.pickle"), 'wb') as outp:
        pickle.dump(rec_dataset, outp, pickle.HIGHEST_PROTOCOL)
    
    model=pre_processing_args.llm_model
    begin_user=0
    count=begin_user
    users=rec_dataset.users
    users=users[begin_user:]
    for user_key in users:
          
          count+=1
          if count==101: break
          
          #task-3 get title and label
          history_item_title,recommend_item_title=get_history_item_title(user_key,rec_dataset)          
          recommend_item_label=Interest_classification(history_item_title,recommend_item_title)

          #task-4 retrive history item information
          rec_item_information,history_item_information,user_review_on_rec,history_item_review,rec_item_other_user_review,user_history_review=All_rec_history_data_process(user_key,rec_dataset)
          num_len=len(history_item_title)
          history_item_discrimination={}
          for key,item in history_item_information.items():
              item_infor=Item_discrimination(item)
              history_item_discrimination[key]=item_infor
          
          rec_item_discrimination= Item_discrimination(rec_item_information)   
          print("finished rec_item_discrimination")    
          
          #task-5 regenerate history item title
          history_reconstruct_title=History_reconstruction(history_item_discrimination)
          print("finished history_reconstruct_title")
          
          #task-all get final explaination          
          RecExplanation=Rec_explanation(recommend_item_label,rec_item_discrimination,history_item_discrimination)
          print("finished explanation")
                
          #get score
          user_aspects=aspects_model(user_review_on_rec,model)  
          Rec_score=exp_score_model(RecExplanation,user_aspects)   
          print("finished score")
          try:
                Rec_score=int(Rec_score)
          except ValueError:
                Rec_score=Rec_score                  
            
                  
          result={
              'Rec_score':Rec_score,
              'label':recommend_item_label,
              'RecExplainer response':RecExplanation,
            }
          with open('./output/Rec_Explanation/Rec_Cell_Phones_and_Accessories.json', 'a') as file_out:
            json.dump(result,file_out)
            file_out.write(",\n")
          print(f"finished {count}")
          #------------------------------------------------------------------------
                          
          
          
          
  

        
        
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