#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw @ 2025
# @generate at 2025/1/9 10:07
# comment: 处理锻炼数据

import io
import aiohttp
from garmin_fit_sdk import Decoder, Stream
import asyncpg

ins_workout_fits = """insert into public.workout_fits(workout_summary_id,altitude,distance,
                    enhanced_altitude,enhanced_speed,gps_accuracy,grade,position_lat,position_long,speed,
                    temperature,battery_soc,created_at) values %s;
                    """

del_workout_fits = "delete from public.workout_fits where workout_summary_id = $1;"

ins_workout_summary = ("insert into public.workout_summary(id,ascent_accum,distance_accum,"
                       "duration_active_accum,duration_paused_accum,duration_total_accum,speed_avg,"
                       "created_at,updated_at) values($1, $2, $3, $4, $5, $6, $7, $8, $9) "
                       "on conflict (id) do update set ascent_accum=excluded.ascent_accum,"
                       "distance_accum=excluded.distance_accum,"
                       "duration_active_accum=excluded.duration_active_accum,"
                       "duration_paused_accum=excluded.duration_paused_accum,"
                       "duration_total_accum=excluded.duration_total_accum,"
                       "speed_avg=excluded.speed_avg,created_at=excluded.created_at,updated_at=excluded.updated_at;")


async def fetch_file(file_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                return await response.read()
            else:
                print(f"Failed to download file. Status code: {response.status}")
                return None


class WorkoutParser:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def parse_workout(self, in_workouts):
        try:
            workout_summary = in_workouts.get('workout_summary')
            if workout_summary:
                await self.parse_workout_summary(workout_summary)
        except Exception as e:
            print(f"Error parsing workout: {e}")

    async def parse_workout_summary(self, workout_summary):
        try:
            workout_summary_id = workout_summary.get('id')
            files = workout_summary.get('file').get('url')
            if files:
                await self.parse_files(workout_summary_id, files)
            await self.insert_db(ins_workout_summary, (
                workout_summary_id,
                workout_summary.get('ascent_accum'),
                workout_summary.get('distance_accum'),
                workout_summary.get('duration_active_accum'),
                workout_summary.get('duration_paused_accum'),
                workout_summary.get('duration_total_accum'),
                workout_summary.get('speed_avg'),
                workout_summary.get('created_at'),
                workout_summary.get('updated_at')
            ))
        except Exception as e:
            print(f"Error parsing workout summary: {e}")

    async def parse_files(self, workout_summary_id, in_file_url):
        try:
            file_content = await fetch_file(in_file_url)
            if file_content is None:
                print("Failed to download file, skipping parse_fits.")
                return
            file_object = io.BytesIO(file_content)
            await self.parse_fits(workout_summary_id, file_object)
        except Exception as e:
            print(f"Error downloading file: {e}")

    async def parse_fits(self, workout_summary_id, file_object):
        try:
            stream = Stream.from_bytes_io(file_object)
            decoder = Decoder(stream)
            messages, errors = decoder.read()
            record_message = messages.get('record_mesgs')
            if record_message:
                async with self.pool.acquire() as con:
                    async with con.transaction():
                        await con.execute(del_workout_fits, workout_summary_id)
                        ins_values = [
                            (workout_summary_id, record_fit.get('altitude'), record_fit.get('distance'),
                             record_fit.get('enhanced_altitude'), record_fit.get('enhanced_speed'),
                             record_fit.get('gps_accuracy'), record_fit.get('grade'), record_fit.get('position_lat'),
                             record_fit.get('position_long'), record_fit.get('speed'), record_fit.get('temperature'),
                             record_fit.get('battery_soc'), record_fit.get('timestamp'))
                            for record_fit in record_message
                        ]
                        # print("ins_values:", ins_values)
                        # await execute_values(con.cursor(), ins_workout_fits, ins_values, page_size=1000)
                        await con.copy_records_to_table('workout_fits', records=ins_values, columns=[
                            'workout_summary_id', 'altitude', 'distance', 'enhanced_altitude', 'enhanced_speed',
                            'gps_accuracy', 'grade', 'position_lat', 'position_long', 'speed', 'temperature',
                            'battery_soc', 'created_at'
                        ])
        except Exception as e:
            print(f"Error parsing FIT file: {e}")

    async def insert_db(self, query, data):
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(query, *data)
