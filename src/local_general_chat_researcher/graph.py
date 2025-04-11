
import json
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

from local_general_chat_researcher import prompts
from local_general_chat_researcher import utils
from local_general_chat_researcher.state import ChatState

class ResearcherGraph:
    __llm = ChatOllama(model="qwen2.5:3b")

    def __init__(self):
        graph_builder = StateGraph(ChatState)
        
        nodes = [
            {"name": "is_web_search_necessary", "action": self.is_web_search_necessary},
            {"name": "route_based_on_is_web_search_necessary", "action": self.route_based_on_is_web_search_necessary},
            {"name": "extract_query_and_topic", "action": self.extract_query_and_topic},
            {"name": "web_search_and_summarize_results", "action": self.web_search_and_summarize_results},
        ]

        for node in nodes:
            graph_builder.add_node(node.get('name'), node.get('action'))

        graph_builder.set_entry_point("is_web_search_necessary")
        graph_builder.add_conditional_edges(
            "is_web_search_necessary",
            self.route_based_on_is_web_search_necessary
        )
        graph_builder.add_edge("extract_query_and_topic", "web_search_and_summarize_results")
        graph_builder.set_finish_point("web_search_and_summarize_results")

        self.__graph = graph_builder.compile(MemorySaver())


    def is_web_search_necessary(self, chat_state: ChatState) -> ChatState:
        user_prompt = utils.last_message(chat_state).content
        sys_prompt = prompts.check_if_web_search_is_necessary.format_map({
            "current_date": utils.current_date(),
            "user_prompt": user_prompt,
        })
        return ChatState(messages=[self.__llm.invoke([sys_prompt])], last_user_prompt=user_prompt)
    
    
    def route_based_on_is_web_search_necessary(self, chat_state: ChatState) -> ChatState:
        ai_response = utils.last_message(chat_state).content
        if ai_response == "True":
            return "extract_query_and_topic"
        elif ai_response == "False":
            return "chatbot"
        else:
            raise ValueError(f"LLM returned a nonboolean value: {ai_response}")
        

    def extract_query_and_topic(self, chat_state: ChatState) -> ChatState:
        sys_prompt = prompts.generate_query_from_user_prompt.format_map({
            "current_date": utils.current_date(),
            "user_prompt": chat_state["last_user_prompt"]
        })

        return ChatState(messages=[self.__llm.invoke([sys_prompt])])


    def web_search_and_summarize_results(self, chat_state: ChatState) -> ChatState:
        web_search_components = json.loads(utils.last_message(chat_state).content)
        query = web_search_components.get("query")
        topic = web_search_components.get("topic")
        raw_results = utils.web_search(query, topic).get("results")
        results = [{"url": result.get("url"), "content": result.get("raw_content")} for result in raw_results]
        sys_prompt = prompts.summarize_web_search_results.format_map({
            "current_date": utils.current_date(),
            "user_prompt": chat_state["last_user_prompt"],
            "search_result1_url": results[0]["url"],
            "search_result1": results[0]["content"],
            "search_result2_url": results[1]["url"],
            "search_result2": results[1]["content"]
        })
        return ChatState(messages=[self.__llm.invoke([sys_prompt])])

    @property
    def graph(self) -> CompiledStateGraph:
        return self.__graph
    

