from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver


class CustomAgentState(AgentState):  
    name: str
    trip_preference: str
    

agent = create_agent(
    "openai:gpt-5",
    state_schema=CustomAgentState,  
    checkpointer=InMemorySaver(),
    system_prompt = "you are helpful travel assistant and you will be passed in with user name and trip preference from the agent state, use the data to give the best trip recommendations for the given place")
    

# Custom state can be passed in invoke
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello Askar Alaska"}],
        "name": "Askar",  
        "trip_preference": "Alaska"  
    },
    {"configurable": {"thread_id": "1"}})


print(result)



# Custom state can be passed in invoke
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello give me trip recomendation"}],
        "name": "Askar",  
        "trip_preference": "Alaska"  
    },
    {"configurable": {"thread_id": "1"}})


print(result)