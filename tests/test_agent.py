from types import SimpleNamespace

import pytest

from src.app.agent import ModelRuntimeError, route_message_agent
from src.app.departments import Department


def test_route(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.app.agent.agent.invoke",
        lambda _: {"messages": [SimpleNamespace(type="tool", name="send_routed_email", content="IT")]},
    )

    result = route_message_agent("user@example.com", "VPN nie działa")

    assert result is Department.IT


def test_no_tool(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.app.agent.agent.invoke",
        lambda _: {"messages": [SimpleNamespace(type="ai", name=None, content="IT")]},
    )

    with pytest.raises(ModelRuntimeError, match="did not call the email tool"):
        route_message_agent("user@example.com", "Treść wiadomości")


def test_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(_: object) -> None:
        raise RuntimeError("model unavailable")

    monkeypatch.setattr("src.app.agent.agent.invoke", fail)

    with pytest.raises(ModelRuntimeError, match="could not be classified"):
        route_message_agent("user@example.com", "Treść wiadomości")
