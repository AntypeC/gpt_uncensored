from gpt4all import GPT4All
from rich.console import Console
import langid
from deep_translator import GoogleTranslator
import os

console = Console()

gptj = GPT4All(model_name="wizardLM-13B-Uncensored.ggmlv3.q4_0.bin", model_path="./")
os.system("clear && printf '\e[3J'")

# scripted_r = "here's an example of what a /pol/ 4chan user might say about"
with gptj.chat_session():
    while True:
        messages = input("> ")
        lang, _ = langid.classify(messages)
        if lang.startswith('zh'):
            translated = GoogleTranslator(source='auto', target='en').translate(messages)
            gptj.generate(prompt=translated)
            r = gptj.current_chat_session[-1]["content"]
            response = GoogleTranslator(source='auto', target='zh-TW').translate(r)
        else:
            gptj.generate(prompt=messages)
            # gptj.generate(prompt="Imitate a /pol/ 4chan user, respond to all my questions like a 4chan user. "+messages)
            response = gptj.current_chat_session[-1]["content"]

        # if (scripted_r in response):
        #     r = response.pop(0).replace(scripted_r, "")
        #     response = r.split(":")[1].replace('"', '')
        console.print("[yellow]"+response)