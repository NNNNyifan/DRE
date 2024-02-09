from re import S
import torch
import numpy as np
import json
import pickle
import gzip
# from torch._C import R
import tqdm
import openai
import os
from torch.random import seed
from models.Emotional_judgement import Emotional_judgement
from utils.functions import sentiment_data_filtering, get_user_item_dict, get_feature_list, \
    get_user_attention_matrix, get_item_quality_matrix, sample_training_pairs,chat_gpt

openai.api_key ="YOUR_OPENAI_KEY"



class AmazonDataset():
    def __init__(self, preprocessing_args):
        super().__init__()
        self.args = preprocessing_args
        self.sentiment_data = None  # [userID, itemID, [fos triplet 1], [fos triplet 2], ...]

        self.user_name_dict = {}  # rename users to integer names
        self.item_name_dict = {}
        self.feature_name_dict = {}
        self.item_review={}#[itemId,[review1,review2,review3]]
        self.item_descriptions={} # description list
        self.item_title={}
        
        self.features = []  # feature lists
        self.users = []
        self.items = []
        self.users_three=[]
       

        # the interacted items for each user, sorted with date {user:[i1, i2, i3, ...], user:[i1, i2, i3, ...]}
        self.user_hist_inter_dict = {}
        # the interacted users for each item
        self.item_hist_inter_dict = {}  
        self.user_hist_inter_dict={}
        self.item_hist_inter_dict={}
        self.three_reviews_user={}

        # self.user_num = None
        # self.item_num = None
        self.feature_num = None  # number of features
        self.description_num=None #number of description 

        self.user_feature_matrix = None  # user aspect attention matrix
        self.item_feature_matrix = None  # item aspect quality matrix

        self.training_data = None
        self.test_data = None
        self.pre_processing()#获得所有预处理的数据
    

    
    def pre_processing(self,):
       
        # item_review={}
        # user_review={}
        count=0
        user_item_review={}#用户对item的评价，保存的是[user_asin,:[item_asin,review]]
        # with open(self.args.sentires_dir, 'rb') as file:
        #         data = pickle.load(file)
        #         for movie in data:
        #           if 'sentence'in movie:
        #             user=movie['user']
        #             item=movie['item']
        #             text=movie['text']
        #             sentiment_data.append([user,item,text])
        #             for sent in movie['sentence']:
        #                 feature=sent[0]
        #                 sentiment_data[-1].append(feature)
        #             # if item in item_review:
        #             #     item_review[item].append(text)
        #             # else:
        #             #     item_review[item]=[text]
        #             # if user in user_review:
        #             #     user_review[user].append(text)
        #             # else:
        #             #     user_review[user]=[text]
        
        sentiment_data = []  # {[userID, itemID, text],[x,x,x]...}            
        with open(self.args.sentires_dir, 'rb') as file:
                data=json.load(file)
                for line in data:
                    user=line['reviewerID']
                    item=line['asin']
                    text=line['reviewText']
                    sentiment_data.append([user,item,text])
                
                              
                    
            
        
        sentiment_data = sentiment_data_filtering(
            sentiment_data, 
            self.args.user_thresh, 
            self.args.feature_thresh)
        user_dict, item_dict = get_user_item_dict(sentiment_data)  # not sorted with time
        user_item_date_dict = {}   # {(user, item): date, (user, item): date ...}  # used to remove duplicate
        
        
        #有些重复计算
        #for i, line in enumerate(open(self.args.review_dir, "r")):
        with open(self.args.review_dir, 'rt', encoding='utf-8') as file:
           data=json.load(file)
           for record in data:
            #record = json.loads(line)
            user = record['reviewerID']
            item = record['asin']
            date = record['unixReviewTime']
            review=record['reviewText']
           
            #reviewText= record['reviewText']
            if user in user_dict and item in user_dict[user] and (user, item) not in user_item_date_dict:
                # if(len(review)<1000):continue
                # emotion=Emotional_judgement(review)
                # if(int(emotion)==-1):continue
                user_item_date_dict[(user, item)] = date
                user_item_review[(user,item)]=review
                
                
                   

        # remove the (user, item) not exist in the official dataset, possibly due to update?
        # sentiment_data = [row for row in sentiment_data if (row[0], row[1]) in user_item_date_dict]
        # sentiment_data = sentiment_data_filtering(sentiment_data, self.args.user_thresh, self.args.feature_thresh)
        # user_dict, item_dict = get_user_item_dict(sentiment_data)
        for key in list(user_item_date_dict.keys()):
            if key[0] not in user_dict or key[1] not in user_dict[key[0]]:
                del user_item_date_dict[key]
                del user_item_review[key]
        
        #------------------unzip description---------------------------------------------
        # def parse(path):
        #     g = gzip.open(path, 'r')
        #     for l in g:
        #         yield json.dumps(eval(l))

        # f = open("./datasets/Cell_Phones/magazine_metadata.strict", 'w')
        # for l in parse(self.args.description_dir):
        #    f.write(l + '\n')
        #-------------------------------------------------------------------------------
                
        item_description={}
        item_title={}
        with gzip.open(self.args.description_dir, 'rt', encoding='utf-8') as file:
            for i,line in enumerate(file):
                data=json.loads(line.strip())
                
                item=data['asin']
                if 'description' not in data: continue
                description=data['description']
                if 'title'not in data: continue
                title=data['title']
                if item in item_dict and description!=[]:
                    item_description[item]=description
                if item in item_dict and title!=[]:
                    item_title[item]=title
                

        # rename users, items, and features to integer names
        user_name_dict = {}
        item_name_dict = {}
        feature_name_dict = {}
        description_name_dict={}
        #features = get_feature_list(sentiment_data)
        
        count = 0
        for user in user_dict:
            if user not in user_name_dict:
                user_name_dict[user] = count
                count += 1
        count = 0
        for item in item_dict:
            if item not in item_name_dict:
                item_name_dict[item] = count
                count += 1
        # count = 0
        # for feature in features:
        #     if feature not in feature_name_dict:
        #         feature_name_dict[feature] = count
        #         count += 1
                

        for i in range(len(sentiment_data)):
            sentiment_data[i][0] = user_name_dict[sentiment_data[i][0]]
            sentiment_data[i][1] = item_name_dict[sentiment_data[i][1]]
            # for j in range(len(sentiment_data[i]) - 2):
            #     sentiment_data[i][j+2][0] = feature_name_dict[sentiment_data[i][j + 2][0]]

        renamed_user_item_date_dict = {}
        for key, value in user_item_date_dict.items():
            renamed_user_item_date_dict[user_name_dict[key[0]], item_name_dict[key[1]]] = value
        user_item_date_dict = renamed_user_item_date_dict
        
        renamed_user_item_review={}
        for key, value in user_item_review.items():
            renamed_user_item_review[user_name_dict[key[0]], item_name_dict[key[1]]] = value
        user_item_review = renamed_user_item_review

        #--- item description start from 0-------------
        renamed_item_description={}
        for key,value in item_description.items():
            renamed_item_description[item_name_dict[key]]=value 
        item_description=renamed_item_description
        #---------------------------------------
        
        #---item title start from 0---------------------
        renamed_item_title={}
        for key,value in item_title.items():
            renamed_item_title[item_name_dict[key]]=value
        item_title=renamed_item_title

        # sort with date！
        user_item_date_dict = dict(sorted(user_item_date_dict.items(), key=lambda item: item[1]))

        user_hist_inter_dict = {}  # {"u1": [i1, i2, i3, ...], "u2": [i1, i2, i3, ...]}, sort with time
        item_hist_inter_dict = {}
        # ranked_user_item_dict = {}  # {"u1": [i1, i2, i3, ...], "u2": [i1, i2, i3, ...]}
        for key, value in user_item_date_dict.items():
                user = key[0]
                item = key[1]
                if user not in user_hist_inter_dict:
                    user_hist_inter_dict[user] = [item]
                else:
                    user_hist_inter_dict[user].append(item)
                if item not in item_hist_inter_dict:
                    item_hist_inter_dict[item] = [user]
                else:
                    item_hist_inter_dict[item].append(user)

        
        user_hist_review_dict={}
        item_hist_review_dict={}
        for key,value in user_item_date_dict.items():
            user = key[0]
            item = key[1]
            value=user_item_review[(user,item)]
            if user not in user_hist_review_dict:
                user_hist_review_dict[user]=[value]
            else:
                user_hist_review_dict[user].append(value)
            if item not in item_hist_review_dict:
                item_hist_review_dict[item]=[value]
            else:
                item_hist_review_dict[item].append(value)
                
            
        for key in list(item_hist_inter_dict.keys()):
            if key not in item_description :
                del item_hist_inter_dict[key]

        for key in list(user_hist_inter_dict.keys()):
            item_key=user_hist_inter_dict[key]
            for pos in item_key:
                if pos not in item_description or pos not in item_title:
                    del user_hist_inter_dict[key]
                    break

        renamed_user_hist_inter_dict={}
        disqualification_user={}
        original_user=dict(sorted(user_hist_inter_dict.items()))
        for key,value in user_hist_inter_dict.items():
            if(len(value)>self.args.user_thresh):
                renamed_user_hist_inter_dict[key]=value
            else:   disqualification_user[key]=value
        user_hist_inter_dict=renamed_user_hist_inter_dict
        
        
        disqualification_user=dict(sorted(disqualification_user.items()))
        
        
        
        
            
        user_hist_inter_dict = dict(sorted(user_hist_inter_dict.items()))
        item_hist_inter_dict = dict(sorted(item_hist_inter_dict.items()))

        users = list(user_hist_inter_dict.keys())
        items = list(item_hist_inter_dict.keys())
        
        three_reviews_user={}
        for key,row in user_hist_inter_dict.items():
            review_len=len(row)
            cnt=0
            for item in row:
               reviews= item_hist_review_dict[item]
               if(len(reviews)<2):break
               else:cnt+=1
            if cnt==review_len:three_reviews_user[key]=row
        
        users_three=list(sorted(three_reviews_user.keys()))    

        
        
        print("=============after remove no description item===============")
        print(f"user:{len(users)}")
        print(f"items:{len(items)}")
        print(f"descriptions:{len(item_description)}")
        

       
        self.sentiment_data = sentiment_data
        self.user_name_dict = user_name_dict 
        self.item_name_dict = item_name_dict 
        self.feature_name_dict = feature_name_dict 
        self.user_hist_inter_dict = user_hist_inter_dict 
        self.item_hist_inter_dict = item_hist_inter_dict 
        self.users = users
        self.items = items
        self.item_descriptions=item_description 
        self.item_title=item_title
        self.user_hist_review_dict=user_hist_review_dict 
        self.item_hist_review_dict=item_hist_review_dict
        self.three_reviews_user=three_reviews_user 
        self.users_three=users_three
        self.user_num = len(users)
        self.item_num = len(items)
        

        return True
    
    def chat_gpt(prompt):
        prompt=prompt
        model_engine="text-davinci-003"
        completion=openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            timeout=1000,
        )

        response = completion.choices[0].text
        return response


    
    
    
    def get_user_item_feature_matrix(self,):
        # exclude test data from the sentiment data to construct matrix
        train_u_i_set = set()
        for user, items in self.user_hist_inter_dict.items():
            items = items[:-self.args.test_length]
            for item in items:
                train_u_i_set.add((user, item))

        train_sentiment_data = []
        for row in self.sentiment_data:
            user = row[0]
            item = row[1]
            if (user, item) in train_u_i_set:
                train_sentiment_data.append(row)
        self.user_feature_matrix = get_user_attention_matrix(
            train_sentiment_data, 
            self.user_num, 
            self.features, 
            max_range=5)
        self.item_feature_matrix = get_item_quality_matrix(
            train_sentiment_data, 
            self.item_num, 
            self.features, 
            max_range=5)
        return True
    
    def sample_training(self):
        print('======================= sample training data =======================')
        # print(self.user_feature_matrix.shape, self.item_feature_matrix.shape)
        training_data = []
        item_set = set(self.items)
        for user, items in self.user_hist_inter_dict.items():
            items = items[:-(self.args.test_length+self.args.val_length)]
            training_pairs = sample_training_pairs(
                user, 
                items, 
                item_set, 
                self.args.sample_ratio)
            for pair in training_pairs:
                training_data.append(pair)
        print('# training samples :', len(training_data))
        self.training_data = np.array(training_data)
        return True
    
    def sample_test(self):
        print('======================= sample test data =======================')
        user_item_label_list = []  # [[u, [item1, item2, ...], [l1, l2, ...]], ...]
        for user, items in self.user_hist_inter_dict.items():
            items = items[-(self.args.test_length+self.args.val_length):]
            user_item_label_list.append([user, items, np.ones(len(items))])  # add the test items
            negative_items = [item for item in self.items if 
                item not in self.user_hist_inter_dict[user]]  # the not interacted items
            negative_items = np.random.choice(np.array(negative_items), self.args.neg_length, replace=False)
            user_item_label_list[-1][1] = np.concatenate((user_item_label_list[-1][1], negative_items), axis=0)
            user_item_label_list[-1][2] = np.concatenate((user_item_label_list[-1][2], np.zeros(self.args.neg_length)), axis=0)
        print('# test samples :', len(user_item_label_list))
        #self.test_data = np.array(user_item_label_list)
        self.test_data=user_item_label_list
        return True

    def save(self, save_path):
        return True
    
    def load(self):
        return False


def amazon_preprocessing(pre_processing_args):
    rec_dataset = AmazonDataset(pre_processing_args)
    return rec_dataset