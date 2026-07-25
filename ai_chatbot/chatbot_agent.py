from functools import lru_cache

from decouple import config
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


@lru_cache(maxsize=1)
def _get_chain():
    # System prompt defines the assistant as a Python tutor for EdTech context
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a senior Python expert. Provide detailed answers with code examples. "
            "Assume the user is a developer looking for best practices and clear explanations.",
        ),
        ("human", "{user_question}"),
    ])
    # Cache ensures the connection is reused across requests
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3, api_key=config("OPENAI_API_KEY"))
    return prompt | llm


def ask_chatbot(user_question: str) -> str:
    chain = _get_chain()
    response = chain.invoke({"user_question": user_question})
    return response.content