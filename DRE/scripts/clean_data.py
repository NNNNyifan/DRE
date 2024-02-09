import sys
import json
import gzip
import os
from models.Emotional_judgement import Emotional_judgement
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


current_directory = os.getcwd()


absolute_path = os.path.join(current_directory, 'datasets', 'Cell_Phones', 'Cleaned_reviews_Cell_Phones_and_Accessories_5.json')
 
review_dir="./datasets/Cell_Phones/reviews_Cell_Phones_and_Accessories_5.json.gz"
clean_movie_review_dir="./datasets/Cell_Phones/Cleaned_reviews_Cell_Phones_and_Accessories_5.json"
review=[]
cnt=0
with gzip.open(review_dir, 'rt', encoding='utf-8') as file:
           for i, line in enumerate(file):
            if i<152803:continue  #phone:152802
            record = json.loads(line)
            user = record['reviewerID']
            item = record['asin']
            date = record['unixReviewTime']
            if 'reviewText' in record:
              review=record['reviewText']
            else: review={}
            #reviewText= record['reviewText']

            
            if(len(review)<500):continue
            emotion=Emotional_judgement(review)
            
            try:
                emotion_int = int(emotion)

                if emotion_int == -1:
                    continue
                else:
                    data={'reviewerID':user,'asin':item,'unixReviewTime':date,'reviewText':review}
                    with open(absolute_path, "a") as json_file:
                        json.dump(data, json_file)
                        json_file.write(",\n")
                    print(f"Emotion right cnt: {i}")

            except ValueError:
                  print(f"Invalid emotion format for: {emotion}. wrong cnt:{i},Skipping...")
                  
           
                