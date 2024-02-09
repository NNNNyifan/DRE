system = """You are given item's description and reviews.
response item profile using the following format:
item:{item name} 
description: {item desc}
other users' review:{item review}

extract key features from reviews;
item description have to under 100 words.You are not allowed to response any other words for any explanation or note. \
Now, the task formally begins. Any other information should not disturb you.

"""


Q1="""
{
item:Interstellar
description:"Interstellar" is a science fiction film that revolves around a group of astronauts traveling through a wormhole. Faced with Earth's impending catastrophe, this team embarks on a perilous mission to find a new human habitat. The wormhole leads them to star systems far from Earth, exploring potential new homes. In this unknown universe, they encounter the relativistic effects of time, navigate challenges on alien planets, and confront crucial decisions about the fate of humanity. The item blends elements of science, family emotions, and the exploration of the unknown, offering a thought-provoking adventure.
other viewers' reviews: "Interstellar" is a heart-shaking science fiction journey, deeply attracting the audience immersed in the interleaving of time and space and the unknown wonders of the universe. The film skillfully blends deep scientific concepts with touching family emotions, making people ponder the vastness of the universe while also being moved by the tenacity of human nature. The perfect combination of visual effects and music makes every frame a work of art, and Matthew McConaughey's excellent acting adds soul to the story. Overall, this is a fascinating, thoughtful and emotional sci-fi masterpiece.
}
summerize reviews,give item profile.

"""
assistant1="""
item: Interstellar
description:
Interstellar" narrates the thrilling adventure led by former NASA astronaut Cooper and his team as they traverse a wormhole in search of a new habitable planet(item brief introduction). \
The film delves into the intricacies of space-time relativity, the challenges of human survival, the bonds of family and emotions, as well as the mysteries of extraterrestrial life.(item theme)
review:"Interstellar" deep science fiction and family emotion integration, visual shock, music moving, McConaughey's outstanding acting gives the story soul, is a fascinating, thinking and emotional science fiction giant.
"""


Q2="""
{
item:Apple watch Series 2
description:Apple Watch Series 2 is a smart watch with powerful health and exercise tracking functions, water-resistant design for swimming, built-in GPS for accurate positioning, equipped with a bright OLED display, support for a variety of third-party applications, is a portable smart device that combines fashion and technology.
other viewers' reviews:After buying the Apple Watch Series 2, life really feels more convenient and interesting. Not only can you monitor your health status at any time, but you can also record your movement trajectory, and the amount of daily activity is at a glance. I especially like its water-resistant design, which allows me to carry it with me while swimming. The built-in GPS function is very practical when outdoor activities, no longer have to worry about getting lost. Moreover, the stylish look and colorful dial selection make it not only a powerful device, but also part of a fashionable accessory. Overall, Apple Watch has added a lot of fun and convenience to my life.
}
summerize reviews,give item profile
"""

assistant2="""
item:Apple watch Series 2
description:Apple Watch Series 2 combines powerful health and exercise tracking functions, support for water resistance design, built-in GPS for accurate positioning, equipped with bright OLED display, wide support for third-party applications, is a portable smart device that combines fashion and technology.
other viewers' reviews: Apple watch Series 2 Health monitoring and motion tracking function, water resistance design, built-in GPS positioning function, stylish appearance and dial selection, convenient life and practicality.
"""

def recommend_item_profile_prompt(rec_item_information,rec_item_other_user_review):
    message=[]
    
    query2=f"item description:{rec_item_information},item review{rec_item_other_user_review},summerize reviews,give item profile"
    
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": assistant1})
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": assistant2})
    message.append({"role": "user", "content": query2}) 
    
    return  message

def llama_prompt(rec_item_information,rec_item_other_user_review):
    message=[]
    
    query2=f"item description:{rec_item_information},item review{rec_item_other_user_review},summerize reviews,give item profile"
    
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": query2}) 
    
    conversation_str = " ".join([f"{item['role']}: {item['content']}" for item in message])
    return  conversation_str
    
    