import openai
import os
from dotenv import load_dotenv
from pyfzf.pyfzf import FzfPrompt
from rich import print
from rich.console import Console
from rich.markdown import Markdown

fzf = FzfPrompt()
console = Console()
load_dotenv()
openai.api_key = os.getenv("API_KEY")
openai.organization = os.getenv("API_ORG")

GPT_MODELS = [
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-16k',
    'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-0301',
    'gpt-3.5-turbo-16k-0613'
]


def getModel():
    engineList = []
    engines = openai.Engine.list()

    for engine in engines.data:
        engineList.append(engine.id)

    res = fzf.prompt(engineList, "--cycle")
    return res[0]


def prompt(question, model):
    tokens = int(input("enter amount of tokens: "))
    completion = openai.Completion.create(model=model,
                                          prompt=question,
                                          max_tokens=tokens,
                                          temperature=0)

    return completion.choices[0].text


def chat(message, model):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": message}
        ]
    )

    return completion.choices[0].message.content


def help():
    print("[blue]h/help: [white]Gives a list of commands")
    print("[blue]model: [white]show current used model")
    print("[blue]models: [white]allows you to change the current model")
    print("[blue]exit: [white]exits the program")
    print("any other text will be send as a request to openai")


def main():
    model = getModel()
    is_gpt_model = model in GPT_MODELS

    print("openAI CLI")
    print(f"current model in use: [green]{model}")
    print("[blue]h/help: [white]shows list of possible commands")

    while True:
        question = input("> ")

        if question == "h" or question == "help":
            help()
        elif question == "model":
            print(f"current model in use: {model}")
        elif question == "models":
            model = getModel()
            is_gpt_model = model in GPT_MODELS
        elif question == "exit":
            break
        else:
            if is_gpt_model:
                res = chat(question, model)
                markdown = Markdown(res)
                console.print(markdown)
            else:
                res = prompt(question, model)
                markdown = Markdown(res)
                console.print(markdown)


if __name__ == "__main__":
    main()
