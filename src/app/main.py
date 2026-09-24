from fastapi import FastAPI, HTTPException, status

from src.app.agent import ModelRuntimeError, route_message_agent
from src.app.schemas import MessageRequest, RouteResponse

app = FastAPI(
    title="AI Message Router API",
    tags=["Message Routing"],
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
        422: {"description": "Validation error in input data."},
        500: {"description": "Message classification service is unavailable."},
    },
)
def route_message(payload: MessageRequest) -> RouteResponse:
    try:
        department = route_message_agent(str(payload.email), payload.message)
        return RouteResponse(department=department)
    except ModelRuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Message classification service is unavailable",
        ) from e
