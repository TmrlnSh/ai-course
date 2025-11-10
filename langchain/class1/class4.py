from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from typing import Any


@before_model  # Decorator that runs this function before the model processes messages
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]  # Extract the list of messages from the agent state

    if len(messages) <= 3:  # Check if there are 3 or fewer messages
        return None  # No changes needed - return None to indicate no state modification

    first_msg = messages[0]  # Keep the first message (usually the system prompt)
    # Keep last 3 messages if even number of messages, otherwise keep last 4
    # This ensures we maintain conversation pairs (user/assistant turns)
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages  # Combine first message with recent messages

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),  # Signal to remove all existing messages
            *new_messages  # Unpack and add the trimmed messages back
        ]
    }

agent = create_agent(
    "openai:gpt-5",
    middleware=[trim_messages],
    checkpointer=InMemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
result = agent.invoke({"messages": "now do the same but for dogs"}, config)
print(result)

final_response = agent.invoke({"messages": "what's my name?"}, config)
print("=================12")
print(final_response)

final_response["messages"][-1].pretty_print()
"""
================================== Ai Message ==================================

Your name is Bob. You told me that earlier.
If you'd like me to call you a nickname or use a different name, just say the word.
"""