from langchain.agents import create_agent
from langgraph.config import get_stream_writer
from langchain_core.messages import AIMessage, ToolMessage

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)

print("Starting agent stream...\n")

for stream_mode, chunk in agent.stream(  
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["custom", "messages"],
):
    if stream_mode == "custom":
        print(f"Tool: {chunk}")
    
    elif stream_mode == "messages":
        message, metadata = chunk
        
        if isinstance(message, AIMessage) and message.content:
            print(message.content, end="", flush=True)

print()