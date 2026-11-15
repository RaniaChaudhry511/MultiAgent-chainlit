import chainlit as cl
from agents import Runner
from agents_config import content_router
from openai.types.responses import ResponseTextDeltaEvent


def is_quota_error(exc):
    indicators = (
        "429",
        "quota",
        "rate limit",
        "rate_limit",
        "resource_exhausted",
        "resource exhausted",
        "too many requests",
    )
    pending = [exc]
    seen = set()

    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))

        class_name = type(current).__name__.lower().replace("_", "")
        if any(name in class_name for name in ("ratelimit", "quota", "resourceexhausted")):
            return True
        if getattr(current, "status_code", None) == 429:
            return True

        error_text = f"{str(current)} {repr(current)}".lower()
        if any(indicator in error_text for indicator in indicators):
            return True

        if current.__cause__ is not None:
            pending.append(current.__cause__)
        if current.__context__ is not None:
            pending.append(current.__context__)

    return False


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])

    await cl.Message(
        content=(
            "## Content Assistant\n"
            "Ask me to write, review, or research something.\n\n"
            "Try: `Write a short email to my teacher` or "
            "`Review this paragraph for mistakes`."
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("chat_history", [])

    next_input = [
        *history,
        {"role": "user", "content": message.content},
    ]

    async with cl.Step(name="Multi-agent workflow", show_input=True) as step:
        step.input = message.content

        msg = None
        stream_started = False

        try:
            result = Runner.run_streamed(
                content_router,
                next_input,
                max_turns=8,
            )

            msg = cl.Message(content="")

            async for event in result.stream_events():
                if (
                    event.type == "raw_response_event"
                    and isinstance(event.data, ResponseTextDeltaEvent)
                ):
                    await msg.stream_token(event.data.delta)
                    stream_started = True
                elif event.type == "agent_updated_stream_event":
                    step.output = f"Now working: {event.new_agent.name}"
                    await step.update()

            cl.user_session.set(
                "chat_history",
                result.to_input_list(),
            )

            specialist_name = result.last_agent.name

            step.output = f"Completed. Final responding agent: {specialist_name}"

            msg.content = f"**Responding agent:** {specialist_name}\n\n{msg.content}"
            await msg.update()

        except Exception as exc:
            print("Agent run failed:", repr(exc))
            step.output = f"Failed: {type(exc).__name__}"

            error_message = (
                "Sorry, the demo has reached its usage limit for now. "
                "Please try again later. The limit usually resets within 24 hours."
                if is_quota_error(exc)
                else (
                    "Sorry, the agent run failed. "
                    "Check the VS Code terminal for the error, "
                    "then verify your API key, model, and internet connection."
                )
            )

            if msg is not None and stream_started:
                msg.content = error_message
                await msg.update()
            else:
                await cl.Message(content=error_message).send()
            