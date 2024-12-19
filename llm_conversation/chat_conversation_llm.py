import time
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils.calculate_cost import calculate_cost
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory


class ChatConversationLLM:
    def __init__(self, llm):
        self.llm = llm
        self.model_name = llm.model_name

    def chat_model_conversation(self, stream=True):
        print("\n--------------------------------")
        print("Chatting with model: ", self.model_name)
        print("--------------------------------\n")
        chat_history = []
        system_message = "You are a helpful assistant."
        total_cost = 0
        chat_history.append(SystemMessage(content=system_message))
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                break
            chat_history.append(HumanMessage(content=user_input))
            start_time = time.time()
            aggregate = None
            if stream:
                print("AI: ", end="", flush=True)
                for chunk in self.llm.stream(chat_history, stream_usage=True):
                    print(chunk.content, end="", flush=True)
                    aggregate = chunk if aggregate is None else aggregate + chunk
            else:
                response = self.llm.invoke(chat_history)
                aggregate = response
                print(f"AI: {aggregate.content}", end="", flush=True)
            end_time = time.time()
            chat_history.append(AIMessage(content=aggregate.content))
            print("\n\n---METADATA---")
            token_usage = aggregate.usage_metadata
            # 'input_tokens': *, 'output_tokens': *, 'total_tokens': *
            print(f"Input tokens: {token_usage['input_tokens']}")
            print(f"Output tokens: {token_usage['output_tokens']}")
            cost = calculate_cost(
                self.model_name,
                token_usage["input_tokens"],
                token_usage["output_tokens"],
            )
            total_cost += cost
            print(f"Total cost: ${total_cost:.12f}")
            # print the time taken
            print(f"Time taken: {end_time - start_time} seconds")
            print("---END METADATA---")

    def chat_model_conversation_with_save_to_firestore(self, stream=True):
        print("\n--------------------------------")
        print("Chatting with model: ", self.model_name)
        print("--------------------------------\n")
        # SETUP FIREBASE FIRESTORE
        PROJECT_ID = "niubii-mobile-aef07"
        SESSION_ID = "session_new"
        COLLECTION_NAME = "langchain"
        # Initialize Firestore client
        print("Initializing Firestore client...")
        client = firestore.Client(project=PROJECT_ID)
        # Initilize Firestore Chat message history
        chat_history = FirestoreChatMessageHistory(
            collection=COLLECTION_NAME,
            session_id=SESSION_ID,
            client=client,
        )
        print("Chat history initialized.")
        total_cost = 0
        # print the chat history
        if chat_history.messages:
            print("------BEGIN HISTORY------")
            for message in chat_history.messages:
                # print the message type and content
                print(f"{message.type}: {message.content}")
            print("------END HISTORY------")
        else:
            print("No chat history found.")
            chat_history.add_message(
                SystemMessage(content="You are a helpful assistant.")
            )
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                break
            chat_history.add_message(HumanMessage(content=user_input))
            start_time = time.time()
            aggregate = None
            if stream:
                print("AI: ", end="", flush=True)
                for chunk in self.llm.stream(chat_history.messages, stream_usage=True):
                    print(chunk.content, end="", flush=True)
                    aggregate = chunk if aggregate is None else aggregate + chunk
            else:
                response = self.llm.invoke(chat_history.messages)
                aggregate = response
                print(f"AI: {aggregate.content}", end="", flush=True)
            end_time = time.time()
            chat_history.add_message(AIMessage(content=aggregate.content))

            print("\n\n---METADATA---")
            token_usage = aggregate.usage_metadata
            # 'input_tokens': *, 'output_tokens': *, 'total_tokens': *
            print(f"Input tokens: {token_usage['input_tokens']}")
            print(f"Output tokens: {token_usage['output_tokens']}")
            cost = calculate_cost(
                self.model_name,
                token_usage["input_tokens"],
                token_usage["output_tokens"],
            )
            total_cost += cost
            print(f"Total cost: ${total_cost:.12f}")
            # print the time taken
            print(f"Time taken: {end_time - start_time} seconds")
            print("---END METADATA---")
