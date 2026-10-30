# Content Assistant

A multi-agent assistant that helps with writing, reviewing, and research. Type your request and the router automatically picks the right agent.

## Agents

| Agent | What it does |
|---|---|
| Writer | Drafts emails, posts, articles, and stories, or rewrites existing text |
| Reviewer | Checks text or code you have already written and gives feedback on mistakes and improvements |
| Researcher | Explains a topic with background, key points, and a short summary |

Every reply starts with the name of the agent that answered.

## How to use

1. Type your request in the message box below.
2. For a review, paste the text you want checked along with your message.
3. You can refer to earlier messages, since the chat history is remembered during the session.

## Examples

- `Write a short email to my teacher about a late assignment`
- `Review this paragraph: i go to school everyday and learn many thing`
- `Explain what machine learning is`

## Things to know

- The Researcher has no web search. It answers from the model's own knowledge, so please verify important facts yourself.
- The Reviewer gives feedback as short points and does not rewrite your whole text. Ask the Writer if you want a full rewrite.
- You can write in simple English or Roman Urdu.

## Technical details

- Framework: OpenAI Agents SDK
- Model: Gemini
- Interface: Chainlit