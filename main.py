"""
Copyright 2024 lagtrainzzz
This file is part of OpenScratchBot.
OpenScratchBot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
OpenScratchBot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with OpenScratchBot. If not, see <https://www.gnu.org/licenses/>. 
"""

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
