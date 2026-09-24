from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from src.app.config import settings
from src.app.departments import Department
from src.app.prompts import DEPARTMENT_CHOICE_PROMPT
from src.app.tools import send_routed_email


class ModelRuntimeError(RuntimeError):
    """Raised when the message cannot be classified reliably."""


agent = create_agent(
    model=ChatOllama(base_url=settings.ollama_host, model=settings.model_name, temperature=0.0),
    tools=[send_routed_email],
    system_prompt=DEPARTMENT_CHOICE_PROMPT,
    name="email_router",
)


def route_message_agent(sender_email: str, email_content: str) -> Department:
    try:
        result = agent.invoke({
            "messages": [
                HumanMessage(content=(
                    f"Sender email: {sender_email}\n"
                    f"Incoming message:\n{email_content}"
                ))
            ]
        })
    except Exception as e:
        raise ModelRuntimeError("The message could not be classified") from e

    for message in reversed(result["messages"]):
        if message.type == "tool" and message.name == send_routed_email.name:
            try:
                return Department(message.content)
            except ValueError as e:
                raise ModelRuntimeError("The email tool returned an invalid department") from e

    raise ModelRuntimeError("The agent did not call the email tool")
