# Crocodile (Animal Guessing) Game CLI

A terminal game where the LLM acts as a strict Game Master for an animal‑guessing game ("Crocodile"). The model secretly chooses a single animal, gives progressive hints, validates guesses, and manages attempts or a timer. This project includes a streaming CLI and guardrails to keep the word an animal and prevent leaks.

## Features
- Animal‑only target enforced by the system prompt (never switches mid‑round)
- Streaming responses for a snappy terminal experience
- Attempts‑based (default 5) or time‑based rounds
- Strict hinting: no letters, spellings, rhymes, or translations
- Basic safety and input validation (ignore blank/repeat guesses)

## Prerequisites
- Python 3.9+ (3.10+ recommended)
- OpenAI‑compatible API key
  - `OPENAI_API_KEY` (required)
  - `OPENAI_BASE_URL` (optional, for custom endpoints)

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration
Copy the example env and fill in values:
```bash
cp .env.example .env
```
Environment variables:
- `OPENAI_API_KEY`: your API key
- `OPENAI_BASE_URL`: optional custom endpoint
- `CROC_MODEL`: model name, e.g. `gpt-4o-mini` (default sane fallback)
- `CROC_MODE`: `attempts` or `timer` (optional)
- `CROC_ATTEMPTS`: integer attempts, default 5
- `CROC_TIME_SECONDS`: integer seconds if timer mode, default 120
- `CROC_LANG`: preferred language code (e.g., `en`, `ru`)

## Usage
Run the Crocodile game (streaming):
```bash
python main.py
```

Legacy generic chat (non‑game):
```bash
python conversation.py
```

## System Prompt (Animal‑specific)
The CLI loads a strict system prompt that:
- Forces the target to be a single, safe ANIMAL (never generic words)
- Keeps the chosen animal fixed for the whole round
- Enforces attempts‑based (default 5) or timer‑based flow
- Prohibits letters/spellings/rhymes/translations or partial word disclosures
- Provides concise, one‑hint‑per‑turn feedback: Correct / Close / Incorrect / Invalid

## Example Play
```text
$ python main.py
Game Master: Welcome to Crocodile (Animal Edition)! Mode: attempts (5). Language: en.
Hint: It is a nocturnal mammal known for echolocation.
Status: Attempts left: 5. What is your guess?
You: bat
Game Master: Correct! The animal was: bat. Play again? [y/N]
```

## Troubleshooting
- Missing key: ensure `OPENAI_API_KEY` is set (in env or `.env`).
- Bad model name: set `CROC_MODEL` to a valid one (e.g., `gpt-4o-mini`).
- No streaming output: your terminal may buffer; try a different terminal or disable streaming.
- Proxy/self‑hosted: set `OPENAI_BASE_URL`.

## Files
- `main.py`: Streaming Crocodile game entrypoint
- `conversation.py`: Minimal generic chat CLI
- `.env.example`: Example environment variables
- `requirements.txt`: Pinned dependencies

## License
MIT