import smtplib
from email.message import EmailMessage

from src.app.config import settings


def send_email(recipient_email: str, subject: str, body: str, reply_to: str) -> None:
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = settings.server_email
    msg["To"] = recipient_email
    msg["Reply-To"] = reply_to.strip().lower()

    with smtplib.SMTP(settings.mailhog_host, settings.mailhog_port) as server:
        server.send_message(msg)
