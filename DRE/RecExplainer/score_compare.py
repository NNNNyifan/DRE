import json
RecExplain_dir="./output/Rec_Explanation/Rec_Cell_Phones_and_Accessories.json"
Filter_dir="./output/Phone_and_Acc_20date_100.json"
output_dir="./output/Rec_Score/Score__Cell_Phones_and_Accessories.json"

#读取Rec中的Rec_Score
with open(RecExplain_dir,'r') as rec_file:
    data=json.load(rec_file)

RecExplain_score=[]
for row in data:
  RecExplain_score.append(row['Rec_score'])
  
#读取Filter中的filter_Score
with open(Filter_dir,'r') as filter_file:
    data=json.load(filter_file)

filter_score=[]
for row in data:
  filter_score.append(row['filter_score'])
  
for Rec,filter in zip(RecExplain_score,filter_score):
  if Rec>filter:ans=1
  elif Rec<filter:ans=2
  else:ans=0
  result={
  "ans":ans,
  "Rec_score":Rec,
  "filter_score":filter
  }
  with open(output_dir,'a') as output_file:  
     json.dump(result,output_file)
     output_file.write(",\n")
