def email_input(state: dict):

    return state


def classify_intent(state: dict):

    return state


def new_client(state: dict):

    return state


def tech_support(state: dict):

    return state



def billing(state: dict):

    return state


def response(state: dict):
    return state


from langgraph.graph import StateGraph, START, END

from typing import Literal


from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


agent_builder = StateGraph(MessagesState)

def route_intent(state: MessagesState) -> Literal["new_client", "tech_support", "billing"]:
    """Routes to the appropriate handler based on intent"""
    return state['intent']

# Add nodes
agent_builder.add_node("email_input", email_input)
agent_builder.add_node("classify_intent", classify_intent)
agent_builder.add_node("new_client", new_client)
agent_builder.add_node("tech_support", tech_support)
agent_builder.add_node("billing", billing)
agent_builder.add_node("response", response)


agent_builder.add_edge(START, "email_input")
agent_builder.add_edge("email_input", "classify_intent")

agent_builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "new_client": "new_client",
        "tech_support": "tech_support",
        "billing": "billing"
    }
)
agent_builder.add_edge("new_client", "response")
agent_builder.add_edge("tech_support", "response")
agent_builder.add_edge("billing", "response")

agent_builder.add_edge("response", END)

agent = agent_builder.compile()

graph_png = agent.get_graph(xray=True).draw_mermaid_png()
with open("my_graph.png", "wb") as f:
    f.write(graph_png)
print("Graph saved as my_graph.png")