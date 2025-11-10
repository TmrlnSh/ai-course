from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig


checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:gpt-4o",
    middleware=[
        SummarizationMiddleware(
            model="openai:gpt-4o-mini",
            max_tokens_before_summary=4000,  # Trigger summarization at 4000 tokens
            messages_to_keep=10,  # Keep last 20 messages after summary
        )
    ],
    checkpointer=checkpointer,
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
result = agent.invoke({"messages": "now do the same but for dogs"}, config)
print(len(result["messages"]))

print("######################################")
final_response = agent.invoke({"messages": "what's my name?"}, config)

print(len(final_response["messages"]))

final_response["messages"][-1].pretty_print()