system="""analysing user reviews' preferences, identify the top five aspects that user may be most concerned about,the format of which is as below:
These are user care about aspects:
(1)aspect
(2)aspect
(3)aspect
..
(5)aspect

compare two explanation in these five aspects,Choose an explanation with better semantic coherence,you can only give the response in format:
answer:{answer}
reason:{reason}

aspect have to be under three words;
reason have to combine aspect;
answer only can be explanation1\ explanation2,don't use any other words;
You are not allowed to response any other words for any explanation or note. Now, the task formally begins. Any other information should not disturb you.

"""
def score_prompt(final_recommend_exp,gpt_exp,user_review):
    message=[]
    query=f"these are user history review {user_review},explanation1 is {final_recommend_exp},explanation2 is {gpt_exp},give the better explanation"

    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": query}) 
    
    return  message