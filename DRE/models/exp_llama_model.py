from hugchat import hugchat
from hugchat.login import Login
import os

# Log in to huggingface and grant authorization to huggingchat
email="yifanwang993w@gmail.com"
passwd="020307Wyf@"
sign = Login(email, passwd)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)

# Load cookies when you restart your program:
# sign = login(email, None)
# cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.


def exp_llama_model(filter_history_information,summeraize_rec_information,user_profile):
    # Create a ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

    # non stream response
    prompt=f"""
    In the following,you are given user history item,recommend item,user profile information.Combine three type information, You have to make an explanation about recommend item.
    key information: user history item:{filter_history_information}, recommend item: {summeraize_rec_information},user profile:{user_profile}.
    you can response only like follow formate:
    item:...
    recommend reason:...
    ...
    
    Below is an explanation example:
    'item:Apple watch series 2
    recommend reason: Based on your preferences for electronic products that are convenient, efficient, I recommend the Apple Watch Series 2 to you.\
    This wearable device aligns perfectly with your profile, offering a seamless blend of convenience and efficiency in various life scenarios. \
    As you've shown interest in both Casio watches and MacBook Air, the Apple Watch Series 2 shares a common ground with these devices, providing precision, functionality, and a user-centric design.\
    Its lightweight design ensures comfort, and the clear display not only offers at-a-glance information but also enables features like heart rate monitoring and fitness tracking, catering to your preference for wearable devices. Additionally, the waterproof design adds versatility, allowing you to wear it even during activities like swimming. The integration of notifications and the ability to listen to music directly from the watch further enhance its practicality, making it an ideal choice for someone with your electronic product preferences.
    Additionally, your feedback on Casio suggests a preference for a lighter watch. The Apple Watch Series 2 features a lightweight design, meeting your requirements.'
    
    """
    query_result = chatbot.query(prompt)
    #print(query_result)
    return query_result["text"]