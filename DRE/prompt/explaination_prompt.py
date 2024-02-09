
system=""" Now you are a recommender assistant,combined history related items, write a explanation about recommend item, the format of which is as below:

item:{recommend item }
recommend reason:{reason}
...
user history viewing items profiles which mainly describe similarity between recommend item and history items;
The explanation of the recommended film must make use of relevant information from history viewing items and list related history items as much as possible;
you can only resonponse:{item name} and {recommend reason};
explanation must combines history items, recommend item;
"""

Q1="""
recommend item:
{
item: Interstellar
genre: Science Fiction
description:
Interstellar" narrates the thrilling adventure led by former NASA astronaut Cooper and his team as they traverse a wormhole in search of a new habitable planet. \
The film delves into the intricacies of space-time relativity, the challenges of human survival, the bonds of family and emotions, as well as the mysteries of extraterrestrial life.
review:

}

history item:
{
item:"Star Wars", description:"Star Wars" and "Interstellar" belong to the same film genre, both being sci-fi movies; 
item:"Blade Runner",description:"Blade Runner" and "Interstellar" fall into the same film genre, both being sci-fi movies; 
item:"The Black Hole",description:"The Black Hole" and "Interstellar" explore similar themes, emphasizing space-time travel; 
item:"Inception",description:"Inception" and "Interstellar" are both sci-fi movies. 
item:"Gravity",description:Matthew McConaughey, the lead actor from "Gravity," also plays a significant role in "Interstellar." 
}

user profile:{
(1)Star Wars:sci-fi movies
(2)Inception: Christopher Nolan    
(3)The Black Hole:time travel
}
give recommend item an explanation
"""

assistant1="""
response:{item: Interstellar
recommend reason:
Based on your viewing history, I recommend "Interstellar" to you. This movie aligns with your preference for sci-fi .\
It falls within the science fiction genre, \
similar to "Star Wars" and "Blade Runner" in your viewing history. \
"Interstellar" shares a common theme of emphasizing space-time travel with "The Black Hole." It aligns your preference for space-time travel \
Additionally, it is well-received like "Inception" among the movies you've watched. \
The lead actor from a movie you've seen, "Gravity," Matthew McConaughey, also plays a significant role in "Interstellar" which you mentioned that he is your favorite actor.    
}
"""

Q2="""
recommend item:{
item: Apple watch series 2
genre: electronics
description:Apple Watch series 2 and Macbook Air both run very fast, can bring convenience to work and life, improve efficiency, can be used in many life scenarios.
review:Using the Apple Watch Series 2 is just incredibly convenient. Firstly, this watch is so lightweight that wearing it on the wrist feels like nothing. The display is crystal clear, showing all sorts of information at a glance, and it can even monitor heart rate and steps, making me feel like a fitness pro. I particularly love its waterproof design, making it a breeze to wear while swimming. Getting notifications for messages and calls is super handy, no need to constantly fish out my phone. The best part is being able to listen to music – during a run, I can just play my favorite tunes directly from the watch, it's truly exhilarating.
}

history item:
{
Item: Casio watch genre:watch         related information:Apple Watch Series 2 and Casio watches share common ground in delivering precision and functionality. Both offer advanced timekeeping features, fitness tracking capabilities, and a durable design. Whether it's the seamless integration with smartphones on the Apple Watch or the reliable performance of Casio watches, these timepieces cater to users seeking a blend of style and practicality in their daily lives.
Item:Macbook Air  genre: electronics  related information:Apple Watch Series 2 and MacBook Air share a common thread in embodying Apple's commitment to seamless integration and user-centric design. Both devices boast a lightweight and sleek form factor, providing users with a blend of style and portability.
Item:Glasses      genre:accessories   related information: {no related information}
Item:beats headphones  genre:phone accessories  related information: Apple Watch Series 2 and Beats headphones share a common ethos of delivering a premium audio-visual experience within the Apple ecosystem. hile the Apple Watch Series 2 enhances the wearable technology landscape with features like health tracking and notifications, Beats headphones complement this by offering high-quality audio, ensuring users enjoy a comprehensive and immersive Apple experience.  
}
user profile:{
(1)Casio watch:  durable, and suitable for scenarios 
(2)Macbook air: slim and easy to carry
(3)beats headphone: bright color, suitable for daily    
}
give recommend item an explanation
"""

assistant2="""
item:Apple watch series 2
recommend reason:{
Based on your preferences for electronic products that are convenient, efficient, I recommend the Apple Watch Series 2 to you.\
This wearable device aligns perfectly with your profile, offering a seamless blend of convenience and efficiency in various life scenarios. \
As you've shown interest in both Casio watches and MacBook Air, the Apple Watch Series 2 shares a common ground with these devices, providing precision, functionality, and a user-centric design.\
Its lightweight design ensures comfort, and the clear display not only offers at-a-glance information but also enables features like heart rate monitoring and fitness tracking, catering to your preference for wearable devices. Additionally, the waterproof design adds versatility, allowing you to wear it even during activities like swimming. The integration of notifications and the ability to listen to music directly from the watch further enhance its practicality, making it an ideal choice for someone with your electronic product preferences.

Additionally, your feedback on Casio suggests a preference for a lighter watch. The Apple Watch Series 2 features a lightweight design, meeting your requirements.
}
"""




def explaination_prompt(filter_history_information,summeraize_rec_information,user_profile):
    message=[]
    query=f" user history viewing items profiles and other users' review: {filter_history_information}, \
        , recommend item profile:{summeraize_rec_information},give recommend item  an detail explanation combine history items informations."

    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": assistant1}) 
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": assistant2}) 
    message.append({"role": "user", "content": query}) 
    
    return  query,message

def gpt_prompt(history_item_information,rec_item_infromation):
    message=[]
    query=f"user history viewing items and other users' reviews:{history_item_information} \n, recommend item profile:{rec_item_infromation} and other users' reviews:{rec_item_other_user_review} \n, give recommend item  an detail explanation combine history items informations"
    
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q1}) 
    message.append({"role": "assistant", "content": assistant1}) 
    message.append({"role": "user", "content": Q2}) 
    message.append({"role": "assistant", "content": assistant2}) 
    message.append({"role": "user", "content": query}) 
    
    return  message