from datetime import datetime
from langchain_core.messages import BaseMessage
from tavily import TavilyClient

from local_general_chat_researcher.state import ChatState


def last_message(chat_state: ChatState) -> BaseMessage:
    return chat_state["messages"][-1]
    

def current_date():
    return datetime.now().strftime("%Y-%m-%d")


def web_search(query: str, topic: str):
    client = TavilyClient()
    return client.search(
        query,
        topic=topic,
        max_results=2,
        include_raw_content=True
    )