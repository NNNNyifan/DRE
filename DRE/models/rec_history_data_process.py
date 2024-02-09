

def history_data_process(rec_dataset, rec_item_asin, rec_user_ID):
    rec_user_key=rec_dataset.user_name_dict[rec_user_ID]
    rec_user_history_item_key=rec_dataset.user_hist_inter_dict[rec_user_key]
    history_item_and_review={}
    #descriprion+review
    for key in rec_user_history_item_key:
        history_item_and_review[key] = {
            'description': rec_dataset.item_descriptions.get(key),
            'review': rec_dataset.item_review.get(key)
        }
        
        
    return history_item_and_review


    return history_data_information

def rec_history_data_process(rec_dataset, rec_item_asin, rec_user_ID):
    #正式使用
    # rec_item_key = rec_dataset.item_name_dict[rec_item_asin]
    # rec_item_information = {}
    # rec_item_description = rec_dataset.item_descriptions[rec_item_key]
    # rec_item_review = rec_dataset.item_review[rec_item_key]
    # rec_item_information['description'] = rec_item_description
    # rec_item_information['review'] = rec_item_review
    
    histroy_item_information=history_data_process(rec_dataset, rec_item_asin, rec_user_ID)
    

    last_item_key = list(histroy_item_information.keys())[-1]
    rec_item_information=histroy_item_information[last_item_key]

    histroy_item_information.pop(last_item_key)
    
    return rec_item_information,histroy_item_information

def get_history_item_title(user_key,rec_dataset):
    history_item_title={}
    
    rec_user_history_item_key=rec_dataset.user_hist_inter_dict[user_key]
    for key in rec_user_history_item_key:
        history_item_title[key] = {
            'title':rec_dataset.item_title[key],
        }
    last_item_key = list(history_item_title.keys())[-1]
    

    recommend_item_title=history_item_title[last_item_key]
    history_item_title.pop(last_item_key)
    
    return history_item_title,recommend_item_title
    

    
        
    

def All_history_data_process(user_key,rec_dataset,review_num):
    rec_user_history_item_key=rec_dataset.user_hist_inter_dict[user_key]
    #rec_user_history_item_key=rec_user_history_item_key[-4:]  
    #for key in rec_user_history_item_key:
    histroy_item_information={}
    history_item_review={}
    #descriprion+review
    for key in rec_user_history_item_key:
        histroy_item_information[key] = {
            'title':rec_dataset.item_title[key],
            'description': rec_dataset.item_descriptions[key],
        }

        temp=rec_dataset.item_hist_review_dict[key]
        #history_item_review[key]=temp[:review_num]
        history_item_review[key]=temp[:5]
    
        renamed_user_review=[]
        user_review = rec_dataset.user_hist_review_dict[user_key]
        for review,key in zip(user_review,rec_user_history_item_key):
            title=rec_dataset.item_title[key]
            renamed_user_review.append([title,review])
        user_review=renamed_user_review
        
    return histroy_item_information,history_item_review,user_review


      
    
def All_rec_history_data_process(user_key,rec_dataset,review_num)
    histroy_item_information,history_item_review,user_review=All_history_data_process(user_key,rec_dataset,review_num)
    
    last_item_key = list(histroy_item_information.keys())[-1]
    rec_item_information=histroy_item_information[last_item_key]
    rec_item_other_user_review=history_item_review[last_item_key]
m
    histroy_item_information.pop(last_item_key)
    history_item_review.pop(last_item_key)
    

    user_review_on_rec = user_review[-1] 
    user_history_review=user_review
    user_history_review.pop()
    #user_review.pop()
    
    
    #取出其他用户对推荐电影的评价,
    for index, value in enumerate(rec_item_other_user_review):
        if(value==user_review_on_rec[1]):
          del rec_item_other_user_review[index]
    
    
             
    return rec_item_information,histroy_item_information,user_review_on_rec,\
        history_item_review, rec_item_other_user_review, user_history_review


    