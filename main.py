from dotenv import load_dotenv
from utils.cli_choose_model import cli_choose_model_provider_and_return_llm
from llm_conversation.chat_conversation_llm import ChatConversationLLM

load_dotenv()


if __name__ == "__main__":
    llm = cli_choose_model_provider_and_return_llm()
    chat_conversation_llm = ChatConversationLLM(llm)
    chat_conversation_llm.chat_model_conversation(stream=True)
