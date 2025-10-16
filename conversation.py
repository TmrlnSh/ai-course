from openai import OpenAI
import os


def main():
    client = OpenAI()
    system_prompt = open("crocodile_prompt").read()
    messages = [{"role": "system", "content": system_prompt}]

    print("Chat started. Type /reset to clear, /exit to quit.")
    while True:
        user_input = input("You: ")
        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "bye", "/exit", "/quit", "/bye"}:
            print("Goodbye!")
            break

        if user_input.lower() in {"reset", "/reset"}:
            messages = [{"role": "system", "content": system_prompt}]
            print("Conversation reset.")
            continue
        messages.append({"role": "user", "content": user_input})

        try:
            resp = client.chat.completions.create(
                model="gpt-5",
                messages=messages,
            )
            reply = resp.choices[0].message.content
        except Exception as e:
            reply = f"Error: {e}"

        print(f"Assistant: {reply}\n")
        messages.append({"role": "assistant", "content": reply})
        
if __name__ == "__main__":
    main()
