from unittest.mock import Mock

from src.app.departments import Department
from src.app.tools import send_routed_email


def test_send(monkeypatch) -> None:
    send_email = Mock()
    monkeypatch.setattr("src.app.tools.send_email", send_email)

    result = send_routed_email.invoke({
        "department": Department.HR.value,
        "sender_email": " User@Example.COM ",
        "message": "Czy firma finansuje kursy?",
    })

    assert result == Department.HR.value
    send_email.assert_called_once_with(
        recipient_email=Department.HR.info.email,
        subject="Redirected message from  User@Example.COM ",
        body="Czy firma finansuje kursy?",
        reply_to=" User@Example.COM ",
    )
