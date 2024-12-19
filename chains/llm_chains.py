from langchain.llms import BaseLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import (
    RunnableLambda,
    RunnableSequence,
    RunnableParallel,
    RunnableBranch,
)
from utils.calculate_cost import calculate_cost


class LLMChains:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def basic_chain(self):
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are facts expert who knows facts about {animal}."),
                ("human", "Tell me {fact_count} facts"),
            ]
        )
        chain = prompt_template | self.llm | StrOutputParser()
        return chain

    def sequential_chain(self):
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert with 10 years of experience teaching English communication, "
                    "provide {count} question phrases, and when to use these questions?. "
                    "ONLY ANSWER RELATED TO THE TOPIC {topic}. "
                    "The answer must be written in English.",
                ),
            ]
        )
        translate_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a translator who translates English to {language}.",
                ),
                ("human", "Translate this text to {language}: {text}"),
            ]
        )

        format_first_prompt = RunnableLambda(
            lambda x: prompt_template.format_messages(**x)
        )
        invoke_first_llm = RunnableLambda(lambda x: self.llm.invoke(x))
        parse_first_output = RunnableLambda(
            lambda x: (
                input_tokens := x.usage_metadata["input_tokens"],
                output_tokens := x.usage_metadata["output_tokens"],
                print(
                    f"\n---Input tokens: {input_tokens}, Output tokens: {output_tokens}, Total cost: ${calculate_cost(self.llm.model_name, input_tokens, output_tokens):.10f}---\n"
                ),
                print(x.content),
                x.content,
            )[-1]
        )

        format_translate_prompt = RunnableLambda(
            lambda x: translate_prompt.format_messages(text=x, language="Vietnamese")
        )
        invoke_translate_llm = RunnableLambda(lambda x: self.llm.invoke(x))
        parse_translate_output = RunnableLambda(
            lambda x: (
                input_tokens := x.usage_metadata["input_tokens"],
                output_tokens := x.usage_metadata["output_tokens"],
                print(
                    f"\n---Input tokens: {input_tokens}, Output tokens: {output_tokens}, Total cost: ${calculate_cost(self.llm.model_name, input_tokens, output_tokens):.10f}---\n"
                ),
                x.content,
            )[-1]
        )

        return RunnableSequence(
            first=format_first_prompt,
            middle=[
                invoke_first_llm,
                parse_first_output,
                format_translate_prompt,
                invoke_translate_llm,
            ],
            last=parse_translate_output,
        )

    def parallel_chain(self):
        """Create a parallel chain that runs multiple prompts simultaneously"""
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant who generates content about {country}.",
                ),
                ("human", "Generate list of popular food in {country}."),
            ]
        )

        translate_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant who generates content about {country}.",
                ),
                ("human", "Generate list of popular landscape in {country}."),
            ]
        )

        food_chain = RunnableLambda(
            lambda x: (
                input_tokens := x.usage_metadata["input_tokens"],
                output_tokens := x.usage_metadata["output_tokens"],
                print(
                    f"\n---Input tokens: {input_tokens}, Output tokens: {output_tokens}, Total cost: ${calculate_cost(self.llm.model_name, input_tokens, output_tokens):.10f}---\n"
                ),
                x.content,
            )[-1]
        )
        landscape_chain = RunnableLambda(
            lambda x: (
                input_tokens := x.usage_metadata["input_tokens"],
                output_tokens := x.usage_metadata["output_tokens"],
                print(
                    f"\n---Input tokens: {input_tokens}, Output tokens: {output_tokens}, Total cost: ${calculate_cost(self.llm.model_name, input_tokens, output_tokens):.10f}---\n"
                ),
                x.content,
            )[-1]
        )

        food_chain = prompt_template | self.llm | food_chain
        landscape_chain = translate_prompt | self.llm | landscape_chain

        return RunnableParallel(
            food=food_chain, landscape=landscape_chain
        ) | RunnableLambda(lambda x: x["food"] + "\n" + x["landscape"])

    def conditional_chain(self):
        """Create a conditional chain that classifies feedback and routes to different responses"""
        classifier_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a feedback classifier. Classify the feedback as either POSITIVE or NEGATIVE. MUST RETURN ONLY POSITIVE OR NEGATIVE.",
                ),
                ("human", "Classify this feedback: {feedback}"),
            ]
        )

        positive_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a customer service agent responding to positive feedback.",
                ),
                (
                    "human",
                    "Write a response thanking the customer for their positive feedback: {feedback}",
                ),
            ]
        )

        negative_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a customer service agent responding to negative feedback.",
                ),
                (
                    "human",
                    "Write an empathetic response addressing the negative feedback: {feedback}",
                ),
            ]
        )

        email_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a professional email writing assistant. Write a clear, concise, and professional email that effectively communicates the message while maintaining appropriate tone and formality.",
                ),
                (
                    "human",
                    "Write an email for content: {content} with name: HieuBui, position: Tech Lead, company: 7-Productions",
                ),
            ]
        )
        # Classification chain
        classify_chain = classifier_prompt | self.llm | StrOutputParser()

        # Response chains
        positive_chain = positive_prompt | self.llm | StrOutputParser()
        negative_chain = negative_prompt | self.llm | StrOutputParser()
        email_chain = email_prompt | self.llm | StrOutputParser()
        # Branch based on classification
        branch = RunnableBranch(
            (lambda x: "POSITIVE" in x.upper(), positive_chain),
            (lambda x: "NEGATIVE" in x.upper(), negative_chain),
            (lambda x: positive_chain),
        )
        combine_chain = classify_chain | branch | email_chain
        return combine_chain
