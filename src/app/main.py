import logging

from fastapi import FastAPI, HTTPException, status

from src.app.agent import DepartmentClassificationError, choose_department
from src.app.emails import send_email
from src.app.schemas import MessageRequest, RouteResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Message Router API",
    description="PoC of an AI-powered message routing service using LangGraph and Ollama",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url=None,
    openapi_url="/api/v1/openapi.json",
)


@app.post(
    "/api/v1/route-message",
    response_model=RouteResponse,
    status_code=status.HTTP_200_OK,
    summary="Route a message to the appropriate department",
    responses={
        200: {"description": "Message has been successfully classified and sent."},
        422: {"description": "Validation error in input data (e.g., invalid email)."},
        503: {"description": "Message classification service is unavailable."},
        500: {"description": "Internal server error during email sending."},
    },
)
def route_message(payload: MessageRequest) -> RouteResponse:
    try:
        department = choose_department(payload.message)
        logger.info("Message classified", extra={"department": department.name})
    except DepartmentClassificationError as e:
        logger.exception("Message classification failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Message classification service is unavailable",
        ) from e

    try:
        logger.info("Sending routed message", extra={"department": department.name})
        send_email(
            recipient_email=department.info.email,
            subject=f"Redirected message from {payload.email}",
            body=payload.message,
            reply_to=payload.email
        )
        logger.info("Routed message sent", extra={"department": department.name})

        return RouteResponse(
            department=department
        )
    except Exception as e:
        logger.exception("Failed to send routed message")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email to {department.info.email}"
        ) from e
