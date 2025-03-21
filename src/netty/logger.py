"""Copyright 2024 wangxin.jeffry@gmail.com
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from logging.config import dictConfig

LOGGING = {
    "version": 1,
    "disable_existing_loggers": 0,
    "formatters": {
        "default": {
            "format": "%(asctime)s|%(levelname)s|%(filename)s:%(funcName)s:%(lineno)d|%(message)s",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {"": {"handlers": ["stdout"], "level": "INFO", "propagate": True}},
}


def configure_logging() -> None:
    dictConfig(LOGGING)
