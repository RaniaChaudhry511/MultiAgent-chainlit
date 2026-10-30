import chainlit as cl
from agents import Runner
from agents_config import content_router
from openai.types.responses import ResponseTextDeltaEvent


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

            await cl.Message(
                content=(
                    "Sorry, the agent run failed. "
                    "Check the VS Code terminal for the error, "
                    "then verify your API key, model, and internet connection."
                )
            ).send()
            