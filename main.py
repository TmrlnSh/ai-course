from __future__ import annotations

from typing import List, Dict, Any, Optional
from openai import OpenAI
import os
import sys


def read_system_prompt(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        # Fallback minimal prompt if file is missing
        return (
            "You are the Crocodile Game Master for an ANIMAL-guessing game. "
            "Choose one animal, keep it fixed for the round, and start with a first clue. "
            "No letters/spellings/rhymes/translations; attempts mode (5)."
        )


def stream_chat_completion(client: OpenAI, model: str, messages: List[Dict[str, str]]) -> str:
    """
    Send a chat completion request with streaming and print tokens as they arrive.
    Returns the final concatenated assistant message content.
    """
    buffer: List[str] = []
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        for event in stream:
            delta = getattr(getattr(event, "choices", [None])[0], "delta", None)
            if not delta:
                continue
            chunk = getattr(delta, "content", "") or ""
            if chunk:
                buffer.append(chunk)
                sys.stdout.write(chunk)
                sys.stdout.flush()
        print("\n")
    except Exception as e:
        msg = f"Error during streaming: {e}"
        print(msg)
        return msg
    return "".join(buffer)


def safe_input(prompt: str) -> Optional[str]:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        return None


def main() -> None:
    client = OpenAI()
    model = os.getenv("CROC_MODEL", "gpt-4o-mini")
    lang = os.getenv("CROC_LANG", "en")

    system_prompt_path = "crocodile_prompt"
    system_prompt = read_system_prompt(system_prompt_path)

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
    ]

    print("Crocodile (Animal Edition). Type /reset to restart, /exit to quit.")
    # Trigger initialization: have the model choose an animal and give the first clue
    init_user = (
        f"Start a new round in language: {lang}. Use attempts mode (5). "
        "Choose a random animal and give the first clue now."
    )
    messages.append({"role": "user", "content": init_user})
    print("Game Master: ", end="")
    first_reply = stream_chat_completion(client, model, messages)
    messages.append({"role": "assistant", "content": first_reply})

    while True:
        user_input = safe_input("You: ")
        if user_input is None:
            break
        raw = user_input.strip()
        if not raw:
            print("Game Master: Please enter a non-empty guess or command.\n")
            continue

        cmd = raw.lower()
        if cmd in {"exit", "quit", "bye", "/exit", "/quit", "/bye"}:
            print("Goodbye!")
            break
        if cmd in {"reset", "/reset"}:
            messages = [{"role": "system", "content": system_prompt}]
            print("Game Master: New round starting...\nGame Master: ", end="")
            messages.append({"role": "user", "content": init_user})
            first_reply = stream_chat_completion(client, model, messages)
            messages.append({"role": "assistant", "content": first_reply})
            continue

        messages.append({"role": "user", "content": user_input})
        print("Game Master: ", end="")
        reply = stream_chat_completion(client, model, messages)
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()



