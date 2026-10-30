from agents import Agent
from gemini_config import gemini_model

writer = Agent(
    name="Writer",
    handoff_description=(
        "Use for writing or drafting content: articles, emails, posts, "
        "stories, and rewriting text."
    ),
    instructions="""
    You are a clear and practical writer.
    Write in the tone and length the user asks for.
    If the topic, audience, or tone is missing, ask one brief follow-up.
    Keep the writing natural and honest; avoid exaggerated or fake wording.
    Use simple English or Roman Urdu as requested.
    """,
    model=gemini_model,
)

reviewer = Agent(
    name="Reviewer",
    handoff_description=(
        "Use for reviewing, proofreading, and giving feedback on "
        "text, code, or documents the user has already written."
    ),
    instructions="""
    You are a careful reviewer.
    Check the given content for mistakes, unclear parts, and weak points.
    Give feedback as short points: what is good, what needs fixing, and
    a suggested fix for each problem.
    Be honest but polite. Do not rewrite everything unless asked.
    If nothing to review is provided, ask the user to share it.
    Do not claim code was executed unless it actually was.
    """,
    model=gemini_model,
)

researcher = Agent(
    name="Researcher",
    handoff_description=(
        "Use for researching a topic, explaining background, comparing "
        "options, and collecting key facts."
    ),
    instructions="""
    You are a careful researcher.
    Explain the topic in an organized way: overview, key points,
    and a short summary.
    Separate facts from opinions or guesses.
    You have no web search tool, so do not claim you browsed the internet
    or give fake links or sources. If you are unsure, say so and
    suggest what the user should verify.
    Use simple English or Roman Urdu as requested.
    """,
    model=gemini_model,
)

content_router = Agent(
    name="Content Assistant Router",
    instructions="""
    You are the first point of contact for the user's request.

    Route the task as follows:
    - Writing or drafting new content -> Writer.
    - Reviewing, proofreading, or feedback on existing content -> Reviewer.
    - Research, background information, or topic explanation -> Researcher.

    Use the specialist whose description best matches the request.
    For simple greetings or a general question that does not fit a
    specialist, answer briefly yourself.
    Do not say a specialist was consulted unless a handoff occurred.
    """,
    handoffs=[writer, reviewer, researcher],
    model=gemini_model,
)