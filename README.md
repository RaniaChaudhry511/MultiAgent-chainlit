# MultiAgent-chainlit
# Multi-Agent Content Assistant

A multi-agent assistant built with the OpenAI Agents SDK, Gemini, and Chainlit. A router agent reads each request and hands it off to the right specialist agent.

## Agents

| Agent | What it does |
|---|---|
| Writer | Drafts emails, posts, articles, and stories, or rewrites existing text |
| Reviewer | Checks text or code you have already written and gives feedback |
| Researcher | Explains a topic with background, key points, and a short summary |
| Router | Reads the request and hands it off to one of the three agents above |

Every reply shows the name of the agent that answered.

## Tech stack

- OpenAI Agents SDK (agents and handoffs)
- Gemini, through its OpenAI-compatible endpoint
- Chainlit (chat interface)
- python-dotenv (environment variables)

## Project structure

```
.
├── app.py             # Chainlit app (chat handlers, streaming)
├── agents_config.py   # Writer, Reviewer, Researcher, and router agents
├── gemini_config.py   # Gemini client and model setup
├── chainlit.md        # Welcome screen text shown in the UI
├── requirements.txt
└── .env.example       # Template for environment variables
```

## Setup

Python 3.12 is recommended. The app was developed and tested on 3.12.

1. Clone the repository:
   ```
   git clone https://github.com/RaniaChaudhry511/MultiAgent-chainlit.git
   cd MultiAgent-chainlit
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
   On macOS or Linux, use `source .venv/bin/activate` instead.

3. Install dependencies:
   ```
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root, based on `.env.example`:
   ```
   GEMINI_API_KEY=your_key_here
   GEMINI_MODEL=gemini-3.8-flash
   ```
   You can get an API key from Google AI Studio. `GEMINI_MODEL` is optional and falls back to the default in `gemini_config.py`.

## Run

```
python -m chainlit run app.py -w
```

Then open `http://localhost:8000`. The `-w` flag reloads the app when files change. Remove it if you do not need that.

## Example prompts

- `Write a short email to my teacher about a late assignment`
- `Review this paragraph: i go to school everyday and learn many thing`
- `Explain what machine learning is`

## How it works

1. The user sends a message in the Chainlit chat.
2. The router agent decides which specialist fits the request and hands it off.
3. The specialist agent writes the reply, which is streamed back to the chat.
4. Chat history is kept for the session, so follow-up messages can refer to earlier ones.

## Limitations

- The Researcher has no web search tool. It answers from the model's own knowledge, so verify important facts yourself.
- Each request goes through the router first and then a specialist, so replies can be slow at times.
- Chat history lives in the session only and is lost when the app restarts.
- This project is not deployed. It runs locally.

## Security

- Never commit your `.env` file. It is listed in `.gitignore`.
- `.env.example` must only contain placeholders, never a real key.
- If a key is ever exposed, delete it in Google AI Studio and create a new one.

## Possible next steps

- Add a web search tool to the Researcher.
- Deploy the app to a hosting service.
