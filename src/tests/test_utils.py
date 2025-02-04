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

import pytest

from netty.utils.netif import process_interface_name, interfaces_have_same_sub_port_number


@pytest.mark.parametrize(
    ("interface_name", "slot_number", "expected_result"),
    [
        ("Gi0/1", 1, "Gi1/0/1"),
        ("Te0/2", 2, "Te2/0/2"),
        ("Xg0/3", 1, "Xg1/0/3"),
        ("Xg1/0/1", 2, "Xg2/0/1"),
        ("Te1/0/2", 3, "Te3/0/2"),
        ("g0/0/2", 1, "g1/0/2"),
    ],
)
def test_valid_interface_name(
    interface_name: str, slot_number: int, expected_result: str
) -> None:
    assert process_interface_name(interface_name, slot_number) == expected_result


@pytest.mark.parametrize(
    ("interface_name", "slot_number"),
    [
        ("InvalidInterface", 1),
        ("Gi0/a", 1),
        ("Gi0/", 1),
        ("Gi0", -1),
    ],
)
def test_invalid_interface_name(interface_name: str, slot_number: int) -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        process_interface_name(interface_name, slot_number)


@pytest.mark.parametrize(
    "local_interface, remote_interface, expected",
    [
        ("Gi0/1/1", "Gi0/1/1", True),  # same sub-port number and same format
        ("Gi0/1/1", "Gi0/1/1/1", False),  # same sub-port number and different formats
        ("Gi0/1/1", "Gi0/1/2", False),  # different sub-port numbers and same format
        (
            "Gi0/1/1",
            "Gi0/2/1/1",
            False,
        ),  # different sub-port numbers and different formats
        ("InvalidInterface", "Gi0/1/1", False),  # invalid interface name
        ("Gi0/1", "Gi0/1/1", False),  # interface name missing sub-port number
        ("Gi0/1/1", "Gi0/1", False),  # interface name missing sub-port number
    ],
)
def test_interfaces_have_same_sub_port_number(
    local_interface, remote_interface, expected
):
    assert (
        interfaces_have_same_sub_port_number(local_interface, remote_interface)
        == expected
    )
