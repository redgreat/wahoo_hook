#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw @ 2025
# @generate at 2025/1/9 11:37
# comment: 请求模型

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: int


class File(BaseModel):
    url: str


class Workout(BaseModel):
    id: int
    starts: datetime
    minutes: int
    name: str
    created_at: datetime
    updated_at: datetime
    plan_id: Optional[int] = None
    workout_token: str
    workout_type_id: int


class WorkoutSummary(BaseModel):
    id: int
    ascent_accum: float
    cadence_avg: float
    calories_accum: float
    distance_accum: float
    duration_active_accum: float
    duration_paused_accum: float
    duration_total_accum: float
    heart_rate_avg: float
    power_bike_np_last: float
    power_bike_tss_last: float
    power_avg: float
    speed_avg: float
    work_accum: float
    created_at: datetime
    updated_at: datetime
    file: File
    workout: Workout


class WebhookRequest(BaseModel):
    event_type: str
    webhook_token: str
    user: User
    workout_summary: WorkoutSummary
