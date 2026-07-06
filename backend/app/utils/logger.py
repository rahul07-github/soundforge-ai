"""
Project: SoundForge AI

Module: Logger
"""

import logging

from backend.app.utils.constants import LOG_FORMAT


logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)


logger = logging.getLogger("SoundForge")


def log_info(message: str):
    logger.info(message)


def log_warning(message: str):
    logger.warning(message)


def log_error(message: str):
    logger.error(message)
    