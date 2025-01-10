#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw @ 2025
# @generate at 2025-1-10 12:26:29
# comment: API Routes

from fastapi import APIRouter, HTTPException, status, Request
from utils.request import AppRequest
from models.errors import NotFound
from models.success import Success
from models.workout import WebhookRequest
from utils.workout_parser import WorkoutParser
from http.client import HTTPException
from loguru import logger

router = APIRouter(prefix="/wahoo", tags=["Users"])


@router.post(
    "/workouts",
    response_model=Success,
    responses={404: {"model": NotFound}},
    name="Wenhook CallBack",
)
async def save_workouts(request: AppRequest, webhook_request: Request):
    body = await webhook_request.json()
    logger.info(f"webhook_request_body: {body}")
    if body.get('webhook_token') != request.app.config._config["webhook_token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Webhook Token UnAuthorized!",
        )
    parser = WorkoutParser(request.app.pool)
    await parser.parse_workout(body)

    return {"success": "ok"}
