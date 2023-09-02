from gpt4all import GPT4All
from rich.console import Console
import langid
from deep_translator import GoogleTranslator
import argparse
import os
from gtts import gTTS 

console = Console()
parser = argparse.ArgumentParser()
parser.add_argument("--4chan", dest="fourchan", action="store_true")
args = parser.parse_args()

gptj = GPT4All(model_name="wizardLM-13B-Uncensored.ggmlv3.q4_0.bin", model_path="./")
os.system("clear && printf '\e[3J'")

primary_lang = 'en'
secondary_lang = 'zh-TW'

scripted_r = "here's an example of what a /pol/ 4chan user might say about"
with gptj.chat_session():
    while True:
        messages = input("> ")
        lang, _ = langid.classify(messages)
        if lang.startswith('zh'):
            translated = GoogleTranslator(source='auto', target=primary_lang).translate(messages)
            gptj.generate(prompt=translated)
            r = gptj.current_chat_session[-1]["content"]
            response = GoogleTranslator(source='auto', target=secondary_lang).translate(r)
            voice = gTTS(text=response, lang=secondary_lang, slow=False)
            voice.save('response.mp3')
            os.system('open response.mp3')
        else:
            if args.fourchan:
                # print("4chan")
                messages = "You are now an anonymous user on the 4chan's /pol/ (politically incorrect) board. Speak like one. " + messages
                gptj.generate(prompt=messages)
            else:
                gptj.generate(prompt=messages)
            
            response = gptj.current_chat_session[-1]["content"]

        if (scripted_r in response):
            r = response.pop(0).replace(scripted_r, "")
            response = r.split(":")[1].replace('"', '')
        console.print("[yellow]"+response)