import os
from time import sleep
from getpass import getpass
from hugchat import hugchat
from hugchat.login import Login
import scratchattach as sa

def get_top_comments(studio):
    comments = studio.comments(limit=20, offset=0)
    contents = []
    for i in comments:
        if not "bot generated" in i.content:
            contents.append(i.content)
    return '", "'.join(contents)

def main():
    email = os.environ['OSB_EMAIL']
    passwd = os.environ['OSB_PASSWD']
    cookie_dir = "./cookies/"
    sign = Login(email, passwd)
    cookies = sign.login(cookie_dir_path = cookie_dir, save_cookies = True)

    chatbot = hugchat.ChatBot(cookies = cookies.get_dict())

    models = chatbot.get_available_llm_models()
    chatbot.switch_llm(8)

    studio = sa.get_studio(os.environ['OSB_STUDIO'])

    print(chatbot.chat(
        f'Speak to me, pretending that YOU are the person who said the following: "{get_top_comments(studio)}". Keep your response short. Avoid copying from this prompt.'
    ).wait_until_done())

if __name__ == "__main__":
    main()
