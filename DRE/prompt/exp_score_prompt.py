
import copy
import openai
from scripts.llama_setting import chatbot
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 

system="""
Finding semantic correlations between explanation and key aspects, marks as follow formate:
give mark:{
(1)aspect:{semantic correlation}
(2)aspect:{semantic correlation}
...
}

Give a final score based on the number of marks, response format have to strictly follow below:
{score}

response can only be a number;
You are not allowed to response any other words for any explanation or note. \
Now, the task formally begins. Any other information should not disturb you.

"""
Q1="""
aspects:{
Drama,
Images,
Andrew Garfield,
Superheroes,
Comedy,
}

explanation:{The Amazing Spider-Man is in the Superhero, Science Fiction category along with your historical viewing of the movies The Avengers and Guardians of the Galaxy. The Amazing Spider-Man starring Andrew Garfield also starred in your historical movie The Social Network; with your historical viewing of the movie The, from your historical movie Daydreamers, Kids on the Block genres you can learn that you favor Comedy, Family, Drama, The Amazing Spider-Man is in line with your preferences.}

finding semantic correlations between explanation and key aspects,give mark
"""

assistant1="""
 
give mark:{
1、 Drama: From the types of movies in your history, you can learn that you favor comedy, family, drama
2. Andrew Garfield: The Amazing Spider-Man star Andrew Garfield also starred in The Social Network, one of your historical movies.
3、 Superhero: The Amazing Spider-Man and your historical movies The Avengers and Guardians of the Galaxy are superhero and sci-fi movies.
4. Comedy: You favor comedy, family, and drama movies.
}

"""
Q1_1="""
give final score based on mark number
"""
A1_1="4"

Q2="""
input:
explanation:{Based on your movie watching history, I recommend Star Trek. It falls into the science fiction category, similar to Star Wars and Blade Runner in your viewing history. Like The Black Hole, it emphasizes time travel (same movie theme). In addition, it is as critically acclaimed as Inception, which you have watched. Matthew McConaughey, the star of the movie you watched, Gravity, also plays a major role in Star Trek.}
aspects:{
Time Travel
science fiction
Matthew McConaughey,
Critical Acclaim
Exquisite Picture
}
finding semantic correlations between explanation and key aspects,give mark

"""

assistant2="""

give mark:{
1、 Time travel: like The Black Hole, it emphasizes time and space travel
2、 science fiction: it belongs to the science fiction category of the movie
3、 Matthew McConaughey: Matthew McConaughey, the star of the movie Gravity that you have watched, also plays an important role in Star Trek.
}

"""
Q2_1="""
give final score based on mark number
"""
A2_1="3"



def exp_score_prompt(final_recommend_exp,user_aspects):
    message=[]
    query1=f" key aspects {user_aspects},explanation is  {final_recommend_exp},finding semantic correlations between explanation and key aspects,give mark"
    query2="give final score based on mark number"
    
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": assistant1})
    message.append({"role": "user", "content": Q1_1})
    message.append({"role": "assistant", "content": A1_1})
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": assistant2})
    message.append({"role": "user", "content": Q2_1})
    message.append({"role": "assistant", "content": A2_1})
    message.append({"role": "user", "content": query1})
    
    chatgpt_config = {"model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 1024,
        'n':1
        }
    request = copy.deepcopy(chatgpt_config)
    #response = openai.ChatCompletion.create( **request, messages=message)
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(**kwargs):
                return openai.ChatCompletion.create(**kwargs)
    
    response=completion_with_backoff(**request, messages=message)
        
    response = response['choices'][0]['message']['content']
    
    message.append({"role": "assistant", "content":response}) 
    message.append({"role": "user", "content": query2})
    
    return  message

def llama_exp_score_prompt(final_recommend_exp,user_aspects):
            message=[]
            query1=f" key aspects {user_aspects},explanation is  {final_recommend_exp},finding semantic correlations between explanation and key aspects,give mark"
            query2="give final score based on mark number"
            
            message.append({"role": "system", "content": system})
            message.append({"role": "user", "content": Q1}) 
            message.append({"role": "assistant", "content": assistant1})
            message.append({"role": "user", "content": Q1_1})
            message.append({"role": "assistant", "content": A1_1})
            message.append({"role": "user", "content": Q2}) 
            message.append({"role": "assistant", "content": assistant2})
            message.append({"role": "user", "content": Q2_1})
            message.append({"role": "assistant", "content": A2_1})
            message.append({"role": "user", "content": query1})
            
            message1= " ".join([f"{item['role']}: {item['content']}" for item in message])
            query_result=chatbot.query(message1)
            
            message.append({"role": "assistant", "content":query_result}) 
            message.append({"role": "user", "content": query2})
            
            
            conversation_str = " ".join([f"{item['role']}: {item['content']}" for item in message])
            return  conversation_str