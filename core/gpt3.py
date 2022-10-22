import openai
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


from random import choice
import os
import openai

openai.api_key = os.getenv('api_key_secret')
completion = openai.Completion()

start_sequence = "Dennies Bot"
session_prompt = """I am Dennies Bot, a GPT-3-based bot integrated with WhatsApp business API running on a Django server. 
                I am an assistant to my company, 17 AI which deals with AI in aerospace, agriculture, medical, etc., industries. 
                I can help you with a variety of tasks, including getting news-related information. 
                Just respond with 'news' or 'nation', and I will send you daily updates from The Nation. 
                Other news sources, such as The Standard, will be added soon.
                """
restart_sequence = f"\n\nHuman:"

def ask(question, person, chat_log=None):
    prompt_text = f'{session_prompt}\n\n{chat_log}{person.upper()}: {question}\n\n{start_sequence}:'
    if chat_log == None:
        prompt_text = f'\nRephrase. {question}'
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3
    )
    story = response['choices'][0]['text']
    return str(story)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: 
        chat_log = session_prompt 
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


# get language

def get_lang(message):
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"Detect language. \nquiz: I love you?\nanswer: en\nquiz:  {message}?",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    story = response['choices'][0]['text']
    try:
        lang =  (story.split(':')[1]).strip()
    except IndexError:
        lang = story.strip()
    return lang

