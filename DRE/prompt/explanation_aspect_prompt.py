system="""
from user review extract 5 key aspects which user may pay attention to, the format of which is as below:
aspects:
{
    (1)aspect1
    (2)aspect2
    ...
    (5)aspect5
}
aspects can be movie name and each aspect have to be under three words
"""

Q1="""
input:
review:{This Amazing Spider-Man from Sony has a great plot and I was almost in tears when I saw Gwen die. In terms of production, the graphics are beautifully done, especially the display of Spider-Man's movements, which are very much like real spiders. Andrew Garfield's portrayal of Spider-Man is very much in tune with the comics, with its stature, posture, and expressions all spot on. As an avid fan of the superhero genre, this movie was very much in line with my expectations for Spider-Man. In this movie, Spider-Man shows some funny antics and says some hilarious things from time to time, and the laughs are great.}
explanation:{}
extract five aspects from explanation
"""

assistant1="""

aspects:{
Drama,
Plot,
Andrew Garfield,
Superheroes,
Comedy,
}
"""

Q2="""
input:
review:{The mesmerizing "Star Trek" takes viewers on a fantasy journey through space. Director Christopher Nolan skillfully weaves cosmic exploration, human trials and familial emotions, making the entire story both science fiction and deeply moving. Matthew McConaughey's excellent performance makes the main character's adventures even more fascinating, while the magnificent scenes and visual effects create a marvelous picture of the future. The depiction of black holes in the movie is breathtaking, as if traveling to the abyss of the universe. At the same time, the perfect fusion of music and images further enhances the movie-going experience. Star Trek is not just a sci-fi masterpiece, but also an emotional journey of the heart that makes people think about the courage and wisdom of mankind in exploring the unknown. The movie depicts a universe of infinite possibilities with mind-blowing scenes that mesmerize the audience.}
extract five aspects
"""

assistant2="""
aspects:{
Time Travel
science fiction
Matthew McConaughey,
Critical Acclaim
Exquisite Picture
}

"""

def explanation_aspect_prompt(explanation,user_review):
    message=[]
    query1=f"this is recommend:{explanation},this is user review:{user_review},give five aspects"
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": assistant1})
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": assistant2})
    message.append({"role": "user", "content": query1})

    return message