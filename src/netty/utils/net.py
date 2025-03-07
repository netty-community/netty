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

from ipaddress import IPv4Address


def get_default_dns_server(region: str) -> list[IPv4Address]:
    """
    Get the default dns server of the region, if region is CN, return aliyun public dns server,
    else return google public dns server
    """
    if region == "CN":
        return [IPv4Address("223.5.5.5"), IPv4Address("223.6.6.6")]
    return [IPv4Address("8.8.8.8"), IPv4Address("8.8.4.4")]


def get_default_ntp_server(region: str) -> list[IPv4Address]:
    """
    Get the default ntp server of the region, if region is CN, return aliyun public ntp server,
    else return google public ntp server
    """
    if region == "CN":
        return [IPv4Address("114.118.7.161"), IPv4Address("203.107.6.88")]
    return [IPv4Address("216.239.35.0"), IPv4Address("20.189.79.72")]
