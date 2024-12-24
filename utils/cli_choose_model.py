from utils.constants import ModelProviders
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


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
                pass
            elif provider_selected == ModelProviders.GOOGLE:
                pass
            else:
                print("Provider not supported. Please try again.")
                continue
            break
        except ValueError as e:
            print(f"Please enter a valid number. Error: {e}")
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
            if provider_selected == ModelProviders.GOOGLE:
                llm = ChatGoogleGenerativeAI(model=model_selected, verbose=True)
            elif provider_selected == ModelProviders.OPEN_AI:
                llm = ChatOpenAI(model=model_selected, verbose=True)
            break
        except ValueError as e:
            print(f"Please enter a valid number. Error: {e}")
            continue
    return llm
