from utils.constants import ModelProviders
from langchain_openai import ChatOpenAI


def cli_choose_model_provider_and_return_llm():
    llm = None
    provider_selected = None
    while True:
        print("--------------------------------")
        print("Available providers:")

        for i, provider in enumerate(ModelProviders, 1):
            print(f"{i}. {provider.name}")
        print("--------------------------------")
        try:
            index = int(input("Enter the index of the provider: "))
            if index < 1 or index > len(ModelProviders):
                print("Invalid index. Please try again.")
                continue
            provider_selected = list(ModelProviders)[index - 1]
            if provider_selected == ModelProviders.OPEN_AI:
                llm = ChatOpenAI(temperature=0.6, verbose=True)
            else:
                print("Provider not supported. Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    while True:
        print("--------------------------------")
        print("Available models:")
        models = provider_selected.value
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
        print("--------------------------------")
        try:
            index = int(input("Enter the index of the model: "))
            if index < 1 or index > len(models):
                print("Invalid index. Please try again.")
                continue
            model_selected = models[index - 1]
            llm.model_name = model_selected
            break
        except ValueError:
            print("Please enter a valid number.")
            continue
    return llm
