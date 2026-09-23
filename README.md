# AI Message Router (PoC)

Intelligent email routing microservice powered by **FastAPI**, **LangGraph**, **Ollama**, **MailHog**, and **uv**.

Incoming messages are classified by an autonomous AI Agent using tool/function calling and 
forwarded via SMTP with the original sender set in the `Reply-To` header.

## Quick Start

1. `cp .env.example .env`: configure environment
2. `docker compose up -d --build`: start all services
3. `docker compose logs -f ollama-init`: check model download progress
   *(Ready once `ollama-init` exits with code 0)*
4. `docker compose logs -f`: see all services logs

## Services

- **API Docs (Swagger)**: http://localhost:8000/api/v1/docs
- **MailHog UI**: http://localhost:8025
- **Ollama API**: http://localhost:11434

## Architecture Overview

- **FastAPI**: REST API with OpenAPI/Swagger docs at `/api/v1/docs`.
- **LangGraph**: Stateful graph orchestrating ticket classification and invoking `send_email_tool`.
- **Ollama**: Local LLM engine (auto-pulled on initial boot).
- **MailHog**: SMTP catcher on port 1025 with an interactive Web UI on port 8025.
- **uv**: Fast Python package and dependency manager.

Inspect the received email at http://localhost:8025 to verify the recipient (help-desk@example.com) and the Reply-To header.

## Example Usage

### Test messages

- **HELP_DESK**: `Hej, myszka przestała działać. Macie zapasowe na stanie?`
- **IT**: `Cześć, wyrzuca mi błąd przy logowaniu i nie mam dostępu do bazy produkcyjnej.`
- **KADRY**: `Dzień dobry, wysłałem zwolnienie L4. Proszę o informację, jak wpłynie to na wypłatę.`
- **HR**: `Cześć! W jaki sposób mogę dostać Multisporta dla dziecka?`
- **OTHER**: `Ta firma jest super :)`

Inspect the received email at http://localhost:8025 to verify.
