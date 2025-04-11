
from dataclasses import dataclass
from typing import Annotated

from langgraph.graph.message import add_messages

@dataclass
class ChatState:
    messages: Annotated[list, add_messages]
    last_user_prompt: str = ""
    query: str = ""
    topic: str = ""