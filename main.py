from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from utils.calculate_cost import token_prices
from llm_conversation.chat_conversation_llm import ChatConversationLLM

load_dotenv()


if __name__ == "__main__":
    while True:
        print("Available models:")
        for i, model in enumerate(token_prices):
            print(f"{i+1}. {model}")
        index = int(input("Enter the index of the model: "))
        if index < 1 or index > len(token_prices):
            print("Invalid index. Please try again.")
            continue
        model_name = list(token_prices.keys())[index - 1]
        if model_name in token_prices:
            break
        else:
            print("Model not supported. Please try again.")
    llm = ChatOpenAI(model=model_name, temperature=0.6)
    chat_conversation_llm = ChatConversationLLM(llm)
    chat_conversation_llm.chat_model_conversation_with_save_to_firestore(stream=True)
