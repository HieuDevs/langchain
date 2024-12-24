from dotenv import load_dotenv
from utils.cli_choose_model import cli_choose_model_provider_and_return_llm
from llm_conversation.chat_conversation_llm import ChatConversationLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()


def modify_model(
    llm,
    max_output_tokens: int = 100,
    temperature: float | None = None,
    timeout: int | None = None,
    max_retries: int | None = None,
):
    if isinstance(llm, ChatGoogleGenerativeAI):
        llm.max_output_tokens = max_output_tokens
        if temperature is not None:
            llm.temperature = temperature
        if timeout is not None:
            llm.timeout = timeout
        if max_retries is not None:
            llm.max_retries = max_retries
    elif isinstance(llm, ChatOpenAI):
        llm.max_tokens = max_output_tokens
        if temperature is not None:
            llm.temperature = temperature
        if timeout is not None:
            llm.timeout = timeout
        if max_retries is not None:
            llm.max_retries = max_retries
    return llm


if __name__ == "__main__":
    llm = cli_choose_model_provider_and_return_llm()
    llm = modify_model(llm, max_output_tokens=100)
    # """chat conversation"""
    # chat_conversation_llm = ChatConversationLLM(
    #     llm,
    #     default_system_message="""You are a helpful assistant.
    #     ALWAYS keep your responses under 100 tokens.
    #     Be direct and get straight to the point.
    #     Avoid unnecessary words, pleasantries, or explanations.
    #     Focus only on the most essential information.
    #     """,
    # )
    # chat_conversation_llm.chat_model_conversation(stream=False)
