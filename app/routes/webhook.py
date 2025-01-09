from http.client import HTTPException

from fastapi import APIRouter, HTTPException, status
from utils.request import AppRequest
from models.errors import NotFound
from models.success import Success
from models.workout import WebhookRequest
from utils.workout_parser import WorkoutParser
from loguru import logger

logDir = os.path.expanduser("../logs/")
if not os.path.exists(logDir):
    os.mkdir(logDir)
logFile = os.path.join(logDir, "request.log")
logger.remove(handler_id=None)

logger.add(
    logFile,
    colorize=True,
    rotation="1 days",
    retention="3 days",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
    level="INFO",
)


router = APIRouter(prefix="/wahoo", tags=["Users"])


@router.post(
    "/workouts",
    response_model=Success,
    responses={404: {"model": NotFound}},
    name="Wenhook CallBack",
)
async def save_workouts(request: AppRequest, webhook_request: WebhookRequest):
    if webhook_request.webhook_token != request.app.config._config["webhook_token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Webhook Token UnAuthorized!",
        )

    parser = WorkoutParser(request.app.pool)
    # print("webhook_request:", webhook_request)
    logger.info(f"webhook_request: {webhook_request}")
    await parser.parse_workout(webhook_request)

    return {"success": "ok"}
