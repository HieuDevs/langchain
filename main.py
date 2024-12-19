from dotenv import load_dotenv
from utils.cli_choose_model import cli_choose_model_provider_and_return_llm
from chains.llm_chains import LLMChains

load_dotenv()

if __name__ == "__main__":
    llm = cli_choose_model_provider_and_return_llm()

    """chat conversation"""
    # chat_conversation_llm = ChatConversationLLM(llm)
    # chat_conversation_llm.chat_model_conversation(stream=True)

    """
    chains
    """
    llm_chains = LLMChains(llm)
    chain = llm_chains.conditional_chain()
    negative_review = "The food was terrible!"
    positive_review = "The food was delicious!"
    result = chain.invoke({"feedback": negative_review})
    print(result)
