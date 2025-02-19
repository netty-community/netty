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

import logging
from dataclasses import dataclass


from pydantic import IPvAnyAddress
from netmiko import ConnectHandler, BaseConnection
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
from tcppinglib import tcpping

from netty.arch.platform import Platform

logger = logging.getLogger(__name__)


@dataclass
class ZtpConfPush:
    ip: IPvAnyAddress
    platform: Platform
    username: str
    password: str
    port: int | None = 22

    def __post_init__(self):
        self.netmiko_device_type = self.platform.__str__()
        self.session = self.__session()

    def __ping(self) -> bool:
        """check if target host's ssh connection is available"""
        result = tcpping(address=self.ip.compressed, count=1).is_alive
        return result

    def __session(self) -> BaseConnection | None:
        if self.__ping:
            try:
                return ConnectHandler(
                    **{
                        "host": self.ip,
                        "username": self.username,
                        "password": self.password,
                        "port": self.port,
                        "device_type": self.netmiko_device_type,
                    }
                )
            except (NetmikoAuthenticationException, NetmikoTimeoutException) as e:
                logger.error(f"Error connecting to {self.ip}, error info: {e}")
        return None

    def __disconnect(self):
        if self.session:
            self.session.disconnect()


    def push_config(self, config: str) -> None:
        if self.session:
            self.session.send_config_set(config.splitlines())
            self.__disconnect()
        else:
            logger.error(f"Can't connect to {self.ip}")
            return None
