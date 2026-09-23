import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from src.app.config import settings
from src.app.departments import Department
from src.app.prompts import DEPARTMENT_CHOICE_PROMPT

logger = logging.getLogger(__name__)


class DepartmentClassificationError(RuntimeError):
    """Raised when the message cannot be classified reliably."""


class DepartmentClassification(BaseModel):
    department: Department = Field(
        description="Department to which the email should be routed."
    )


llm = ChatOllama(
    base_url=settings.ollama_host,
    model=settings.model_name,
    temperature=0.0,
).with_structured_output(DepartmentClassification)


def choose_department(email_content: str) -> Department:
    try:
        messages = [
            SystemMessage(content=DEPARTMENT_CHOICE_PROMPT),
            HumanMessage(content=email_content)
        ]

        result = llm.invoke(messages)
        if isinstance(result, DepartmentClassification):
            return result.department
        raise DepartmentClassificationError("The classifier returned an invalid result")

    except Exception as e:
        logger.exception("Error occurred while choosing department")
        raise DepartmentClassificationError("The message could not be classified") from e
