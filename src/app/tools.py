from langchain_core.tools import tool

from src.app.departments import Department
from src.app.emails import send_email


@tool
def send_routed_email(
    department: Department,
    sender_email: str,
    message: str,
) -> str:
    """Send the incoming message to the selected department."""
    send_email(
        recipient_email=department.info.email,
        subject=f"Redirected message from {sender_email}",
        body=message,
        reply_to=sender_email,
    )
    return department.value
