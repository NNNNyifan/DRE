system="""
from user review extract seven key aspects which user may pay attention to, the format of which is as below:
aspects:
{
    (1)aspect1
    (2)aspect2
    ...
    (7)aspect7
}
aspects can be item name and each aspect have to be under three words;
aspects can't be item name.
"""

Q1="""
input:
review:{This Amazing Spider-Man from Sony has a great plot and I was almost in tears when I saw Gwen die. In terms of production, the graphics are beautifully done, especially the display of Spider-Man's movements, which are very much like real spiders. Andrew Garfield's portrayal of Spider-Man is very much in tune with the comics, with its stature, posture, and expressions all spot on. As an avid fan of the superhero genre, this movie was very much in line with my expectations for Spider-Man. In this movie, Spider-Man shows some funny antics and says some hilarious things from time to time, and the laughs are great.}

extract seven aspects
"""

assistant1="""

aspects:{
Drama,
Plot,
Andrew Garfield,
Superheroes,
Comedy,
fan,
hilarious
}
"""

Q2="""
input:
review:{After buying Apple Watch, my life seems to become more exciting and convenient. Not only does it monitor my health, it tracks my exercise data and reminds me to stay active every day like a personal trainer. I especially like its water-resistant design, so that I can wear it to swim at any time, no longer have to worry about the watch will be damaged by water. And the built-in GPS function helps me quickly find my destination when I'm out and about, which is really convenient. Touch the bright OLED display makes interaction more intuitive, and support for a variety of third-party apps makes my wrist a personalized gadget box. Overall, the Apple Watch is really an indispensable smart partner, bringing more fun and convenience to my life.}
extract seven aspects
"""

assistant2="""
aspects:{
Health monitoring;
Water resistance design;
GPS positioning function;
OLED display;
activity tracking;
Exercise tracking;
Third-party apps
}

"""

def aspects_prompt(user_review):
    message=[]
    query1=f"these are user review {user_review},give seven aspects"
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": assistant1})
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": assistant2})
    message.append({"role": "user", "content": query1})

    return message

def llama_aspects_prompt(user_review):
    prompt=f"""
        key information:{user_review}.
        from user review extract seven key aspects which user may pay attention to, the format of which is as below:
        aspects:
        [
            (1)aspect1
            (2)aspect2
            ...
            (7)aspect7
        ]
        aspects can be movie name and each aspect have to be under three words;
        aspects can't be item name.

        """
        
    return prompt