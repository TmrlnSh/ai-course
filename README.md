# AI Conversation CLI

A minimal command-line chat client that talks to an OpenAI-compatible API using the official Python SDK. It maintains conversation history, supports quick commands (reset/exit), and lets you customize the system prompt and model.

## Features
- Maintains full conversation history within the session
- Quick commands: `/reset` to clear history, `/exit` to quit
- Configurable system prompt
- Selectable model (defaults to `gpt-5`)

## Prerequisites
- Python 3.9+ (tested with 3.10+ recommended)
- An OpenAI-compatible API endpoint and API key
  - Default environment variables used by the SDK:
    - `OPENAI_API_KEY` (required)
    - `OPENAI_BASE_URL` (optional; for self-hosted or proxies)

## Installation
1. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install openai
   ```

## Configuration
- Set your API key in your shell environment:
  ```bash
  export OPENAI_API_KEY="YOUR_API_KEY_HERE"
  ```
- If you are using a non-default endpoint (e.g., a proxy or self-hosted server), set:
  ```bash
  export OPENAI_BASE_URL="https://your-endpoint.example.com/v1"
  ```
- Optional: Edit the default system prompt or model in `conversation.py`:
  - System prompt: look for `system_prompt = "..."`
  - Model: look for `model="gpt-5"` in the chat completion call

## Usage
Run the CLI:
```bash
python conversation.py
```
You will see:
```
Chat started. Type /reset to clear, /exit to quit.
```
Type your messages at the `You:` prompt.

### Commands
- `/reset` or `reset`: Clear the current conversation history (retains the system prompt)
- `/exit`, `/quit`, `/bye` (or without slash): Exit the program

## Example Session
```text
$ python conversation.py
Chat started. Type /reset to clear, /exit to quit.
You: Hello!
Assistant: Hi there! How can I help you today?
You: /reset
Conversation reset.
You: What is the capital of Japan?
Assistant: The capital of Japan is Tokyo.
You: /exit
Goodbye!
```

## How It Works
At a high level, the script:
- Instantiates the SDK client: `client = OpenAI()`
- Initializes a messages list with a system prompt
- Appends each user input
- Calls the Chat Completions API with the running `messages`
- Prints the assistant reply and appends it back to `messages`

## Troubleshooting
- Authentication error: Ensure `OPENAI_API_KEY` is exported and valid
- Connection error or 404: If using a proxy or self-hosted endpoint, set `OPENAI_BASE_URL`
- Rate limit or quota errors: Reduce request frequency or check your plan limits
- Unicode or terminal issues: Try a different terminal or locale settings (`export LC_ALL=en_US.UTF-8`)

## Notes
- This is a minimal example intended for learning and quick experiments. For production use, consider adding:
  - Retries/backoff and structured error handling
  - Streaming responses for better UX
  - Config files/flags to control model and system prompt per run
  - Logging and observability

## License
MIT (see your repository’s license if different).