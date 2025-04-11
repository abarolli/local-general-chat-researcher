from datetime import datetime
from langchain_core.messages import BaseMessage

from local_general_chat_researcher.state import ChatState


def last_message(chat_state: ChatState | dict) -> BaseMessage:
    if isinstance(chat_state, dict):
        return chat_state.get("messages")[-1]
    
    return chat_state.messages[-1]


def current_date():
    return datetime.now().strftime("%Y-%m-%d")