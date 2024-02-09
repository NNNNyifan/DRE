from hugchat import hugchat
from hugchat.login import Login
import os
email="EMAIL"
passwd="PASSWORD"
sign = Login(email, passwd)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
# sign.saveCookiesToDir(cookie_path_dir)
# sign = Login(email, None)
cookies = sign.loadCookiesFromDir(cookie_path_dir)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
chatbot2 = hugchat.ChatBot(cookies=cookies.get_dict())
