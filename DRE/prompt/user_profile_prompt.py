


system = """You are asked to describe user interest based on his/her historical reviews,
Please respond only with interests that user may care about in the following format:

 intertest[...]

find out the features that users may pay attention to for the recommended items from the historical reviews;
where interest should be under 50 words . You are not allowed to response any other words for any explanation or note. Now, the task formally begins. Any other information should not disturb you."""

Q="""

(1)Casio Watch: This watch is exceptionally durable, suitable for various scenarios such as swimming, climbing, and more.
(2)Macbook air: This computer is extremely slim, allowing me to carry it and work on the go with ease. This computer is very suitable for my work and improve my work efficiency greatly.
(3)beats headphone: These headphones boast bright colors, making them suitable for everyday outfits. I love it so much!
"""
A="""
(1)Casio watch:  durable, and suitable for scenarios 
(2)Macbook air: slim and easy to carry
(3)beats headphone: bright color, suitable for daily
"""

def user_profile_prompt(user_history_review,rec_item_infromation):
    message=[]
    query=f"user reviews on history items {user_history_review},recommend items:{rec_item_infromation},give user's interests"

    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": Q})
    message.append({"role": "assistant", "content": A})
    message.append({"role": "user", "content": query}) 
   
    
    return  message

def user_profile_llama_prompt(user_history_review,rec_item_infromation):
    prompt = f"""
            key information:user history review:{user_history_review},recommend item information:{rec_item_infromation}.
            You are asked to describe user interest based on his/her historical reviews,
            Please respond only with interests that user may care about in the following format:

            intertest[...]

            find out the features that users may pay attention to for the recommended items from the historical reviews;
            where interest should be under 50 words . You are not allowed to response any other words for any explanation or note. Now, the task formally begins. Any other information should not disturb you.
            """
    return prompt
