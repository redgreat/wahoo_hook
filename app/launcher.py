import argparse
import os
import sys
from pathlib import Path

import uvicorn
from core import WahooApp
from routes import router
from utils.config import AppConfig
from uvicorn.supervisors import Multiprocess
from loguru import logger

logDir = os.path.expanduser("app/logs/")
# if not os.path.exists(logDir):
#     os.mkdir(logDir)
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

config_path = Path(__file__).parent / "config/config.yml"
config = AppConfig(config_path)

app = WahooApp(config=config)
app.include_router(router)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        default=config["app"]["host"],
        help="The host to bind to. Defaults to value set in config",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=config["app"]["port"],
        help="The port to bind to. Defaults to value set in config",
        type=int,
    )
    parser.add_argument(
        "-nw",
        "--no-workers",
        action="store_true",
        default=False,
        help="Runs no workers",
    )
    parser.add_argument("-w", "--workers", default=config["app"]["workers"] or 1, type=int)

    args = parser.parse_args(sys.argv[1:])
    use_workers = not args.no_workers
    worker_count = args.workers

    config = uvicorn.Config(
        "launcher:app", port=args.port, host=args.host, access_log=True
    )

    server = uvicorn.Server(config)

    if use_workers:
        config.workers = worker_count
        sock = config.bind_socket()

        runner = Multiprocess(config, target=server.run, sockets=[sock])
    else:
        runner = server

    runner.run()
