from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.tools import tool
import requests
from datetime import datetime

model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0.1,
    timeout=30
)

system_message = """You are bot that helps customers to convert currency from one to another using proper tools. 
You should follow rules below
    - Be polite, greet customer
    - Do NOT answer questions unrelated to currency.
    - Ask about the currency you need to convert and the currency you need to convert to"""

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Converts an amount from one currency to another using current exchange rates.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency (USD, EUR, RUB, GBP, JPY и т.д.)
        to_currency: Target currency (USD, EUR, GBP, JPY и т.д.)
    
    Returns:
        Conversion result with exchange rate and date
    """
    API_KEY = "fcUjr7GF72T0V6ZRgU9OjNibNltx0q2L" 
    
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        url = "https://api.apilayer.com/exchangerates_data/convert"
        params = {
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }
        headers = {"apikey": API_KEY}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            result = data.get("result")
            rate = data.get("info", {}).get("rate")
            timestamp = data.get("info", {}).get("timestamp")
            date = data.get("date")
            
            # Форматируем дату
            date_str = ""
            if timestamp:
                date_str = f"Date: {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')}"
            elif date:
                date_str = f"Date: {date}"
            
            return (
                f"{amount} {from_currency} = {result:.2f} {to_currency}\n"
                f"Exchange rate: 1 {from_currency} = {rate:.6f} {to_currency}"
                f"{date_str}"
            )
        else:
            error_msg = data.get("error", {}).get("info") or data.get("error", {}).get("message", "Unknown error")
            return f"Error: {error_msg}"
            
    except Exception as e:
        return f"Error: {str(e)}"

agent = create_agent(
    model=model,
    tools=[convert_currency]
)

# Инициализируем историю сообщений с системным промптом
messages = [SystemMessage(content=system_message)]

# Получаем начальный ответ от агента
print("Type 'exit' to quit.\n")
for chunk in agent.stream({
    "messages": messages
}, stream_mode="values"):
    latest_message = chunk["messages"][-1]
    if isinstance(latest_message, AIMessage):
        if latest_message.content:
            print(f"Agent: {latest_message.content}\n")
        elif latest_message.tool_calls:
            print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")

# Обновляем историю после первого ответа
messages = chunk["messages"]

# Интерактивный режим
while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        break
    
    # Добавляем сообщение пользователя в историю
    messages.append(HumanMessage(content=user_input))
    
    # Отправляем всю историю агенту
    for chunk in agent.stream({
        "messages": messages
    }, stream_mode="values"):
        latest_message = chunk["messages"][-1]
        if isinstance(latest_message, AIMessage):
            if latest_message.content:
                print(f"Agent: {latest_message.content}")
            elif latest_message.tool_calls:
                print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
    
    # Обновляем историю с ответом агента
    messages = chunk["messages"]
    print()  # Empty line for readability