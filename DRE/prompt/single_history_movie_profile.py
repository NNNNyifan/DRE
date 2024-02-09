

import copy
import openai


system = """

finish history item profile using similar attributes with recommend item.strictly adhere to the following format when responding:
{   history item:{item name}
    genre:{item genre}
    relevant information:{item information related to recommend item}
    other user' reviews:{summarize review}
}

which relevant information have to under 120 words.
related information mainly describe similarity between history viewing item and recommend item,\
other user' reviews have to under 120 words;
You are not allowed to response any other words for any explanation or note. \
Now, the task formally begins. Any other information should not disturb you."""



Q1="""
history viewing item:
{
    item:Blade Runner
    description:Blade Runner is a classic sci-fi item set in a futuristic Los Angeles that focuses on Blade Runner Rick Deckard as he hunts down Replicants, artificial life forms. During his mission, he begins to have doubts about the emotions and humanity of these machine lifeforms, provoking deep thoughts. The item has become a classic of science fiction movies for its unique visual effects and deep philosophical connotations.
    review:Blade Runner is a mind-blowing experience! That picture of the future world is so powerful, every frame is a work of art. The plot is tight and gripping, and the deep thinking on artificial intelligence and the meaning of life makes me meditate while enjoying it. "Blade Runner" music collocation is also highly emotional, like a feast for the senses. In this imaginative future world, I was not only drawn by the story, but also conquered by its unique aesthetics.
}

recommend item:
{
item: Interstellar
genre: Science Fiction
description:Interstellar" narrates the thrilling adventure led by former NASA astronaut Cooper and his team as they traverse a wormhole in search of a new habitable planet(item brief introduction). \
The film delves into the intricacies of space-time relativity, the challenges of human survival, the bonds of family and emotions, as well as the mysteries of extraterrestrial life.(item theme)   
other user' reviews:Interstellar is a breath-taking sci-fi blockbuster that takes the audience on a magnificent adventure through time and space. The visuals are stunning, the music is moving, and Matthew McConaughey's brilliant performance is deeply touching. The plot is tight, and the discussion of science, family, and human nature is thought-provoking.
}

find similar features between recommend item and history item
"""

A1_1="""
history item: Blade Runner
genre: Science Fiction
related information:In your viewing history, both the film "Blade Runner" and the recommended film "Interstellar" belong to the science fiction genre; \
other user' reviews:they fall under the same film category.Heart-shaking art like pictures, full of a sense of the future of the dream atmosphere, deep human reflection similar with Interstellar
"""

Q2="""
history viewing item:
{
    item:Mac book Air
    description:This slim and portable laptop not only has a stylish look, but also comes with a high-definition Retina display for sharper images and text. Its lightweight design makes it easier to carry around, making it ideal for work and play anywhere. The MacBook Air isn't just brilliant on the outside, it's powerful on the inside. With a fast processor, you can easily multitask, and long battery life means you don't have to worry about power. The keyboard and trackpad are also designed to be extremely comfortable and provide you with an excellent experience.
    reviews:Using an Apple computer is a truly exhilarating experience. First of all, that Retina display is simply dizzying, full of colors and stunning clarity, and every time you open it, it feels like you enter a gorgeous world. The lightweight design allows me to carry it at any time, whether working in a cafe or using it easily on the sofa, without feeling any burden. I was also amazed by the smoothness of the operating system, everything ran so smoothly and naturally. The fast startup speed and stable performance make my work more efficient.
}

recommend item:
{
item: Apple watch series 2 
genre: electronics
description:Apple Watch series 2 and Macbook Air both run very fast, can bring convenience to work and life, improve efficiency, can be used in many life scenarios.
other user' reviews:Using the Apple Watch Series 2 is just incredibly convenient. Firstly, this watch is so lightweight that wearing it on the wrist feels like nothing. The display is crystal clear, showing all sorts of information at a glance, and it can even monitor heart rate and steps, making me feel like a fitness pro. I particularly love its waterproof design, making it a breeze to wear while swimming. Getting notifications for messages and calls is super handy, no need to constantly fish out my phone. The best part is being able to listen to music – during a run, I can just play my favorite tunes directly from the watch, it's truly exhilarating.
}

find similar features between recommend item and history item
"""


A2_1="""
item:Mac book Air
genre: electronics
related information: Mac book Air and Apple watch series 2 both items are functionally characterized by superior display, with the Apple Computer known for its Retina display and the Apple Watch Series 2 also praised for its excellent display performance on a small device. In addition, they focus on efficient and stable performance, providing a convenient work and life experience.
other user' reviews: Both Apple computers and Apple Watch Series 2 emphasize a lightweight design, allowing users to carry them effortlessly anytime. Both feature efficient operating systems and stable performance.Both belong to Apple Brand.
"""


def single_history_movie_profile(item_description,item_review,summeraize_rec_information):
    message=[]
    #item_review=item_review[-2:]
    renamed_item_review=[]
    for review in item_review:
        if len(review)>1500:
            review=review[:1500]
        renamed_item_review.append(review)
    item_review=    renamed_item_review    
            
    query1=f"history item: {item_description} and other user's review in this item{item_review},recommend item profile:{summeraize_rec_information}, find similar features between recommend item and history item ?"
    
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": A1_1}) 
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": A2_1}) 
    message.append({"role": "user", "content": query1}) 
    
    return  message

def llama_single_history_profile(item_description,item_review,summeraize_rec_information):
    message=[]
    query1=f"history item: {item_description} and other user's review in this item{item_review},recommend item profile:{summeraize_rec_information}, find similar features between recommend item and history item ?"
    
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": A1_1}) 
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": A2_1}) 
    message.append({"role": "user", "content": query1}) 
    prompt = " ".join([f"{item['role']}: {item['content']}" for item in message])
    return prompt