import os
import time
import warnings
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence
from langchain_community.document_loaders import PyPDFLoader
from langchain.globals import set_debug
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.callbacks import get_openai_callback

warnings.filterwarnings("ignore")
set_debug(True)
load_dotenv()


# Embed
embeddings = OpenAIEmbeddings()


# Indexing
def load_vector_store(force_recreate=False):
    current_dir = os.getcwd()
    persist_directory = os.path.join(current_dir, "db")
    if os.path.exists(persist_directory) and not force_recreate:
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
        )
    else:
        loader = PyPDFLoader(
            file_path=os.path.join(current_dir, "rag.pdf"),
        )

        docs = loader.load()

        # Split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        texts = text_splitter.split_documents(docs)
        vector_store = Chroma.from_documents(
            texts,
            embeddings,
            persist_directory=persist_directory,
        )
    return vector_store


# Vector Store
vector_store = load_vector_store()

# Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 1},
    # search_type="similarity_score_threshold",
)


if __name__ == "__main__":
    prompt_generate = ChatPromptTemplate.from_template(
        """
    You are an English teacher who answers user input based on the additional information below.
    If the context helps, incorporate it into your explanation to provide the most accurate and thorough answer possible.

    User’s question:
    {user_input}

    Additional information:
    {context}

    Your task:
    - Combine the user’s question with the additional information.
    - Give a clear and detailed response that answers the user’s question as accurately as possible.
    - If the information is not relevant or does not help answer the question, ignore it and answer "I don't know"
    - JUST 3 sentences response
    """
    )
    prompt_checking = ChatPromptTemplate.from_template(
        """You are an experienced and friendly English teacher.
    Your task is to verify if the given response is relevant to the topic.

    Topic: {topic}
    Response: {response}

    Instructions:
    1. Carefully analyze if the response directly addresses the given topic
    2. If the response is NOT relevant to the topic, respond ONLY with "I don't know"
    3. If the response IS relevant to the topic, respond by returning the original response exactly as provided
    4. Do not add any additional commentary or explanations

    Remember: Be strict in your relevance check and maintain the exact format requested.
    """
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    with get_openai_callback() as cb:
        question = "killer"

        # Create RunnableSequence chain
        chain = (
            {
                "context": lambda x: "\n".join(
                    doc.page_content
                    for doc in retriever.get_relevant_documents(x["question"])
                ),
                "user_input": lambda x: x["question"],
            }
            | prompt_generate
            | llm
            | StrOutputParser()
            | (
                lambda x: {
                    "topic": lambda _: "introduce yourself",
                    "response": lambda _: x,
                }
                | prompt_checking
                | llm
                | StrOutputParser()
            )
        )

        # Execute chain
        final_result = chain.invoke({"question": question})
        print(final_result)
        print(f"Tokens Used: {cb.total_tokens}")
        print(f"\tPrompt Tokens: {cb.prompt_tokens}")
        print(f"\tCompletion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost:.8f}")
