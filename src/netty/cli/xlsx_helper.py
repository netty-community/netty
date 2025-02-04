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

import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.cell_range import CellRange

from netty.cli.default import generate_default_device_headers
from netty.arch import Manufacturer, DeviceRole

def index_to_col(index: int) -> str:
    col = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        col = chr(65 + remainder) + col
    return col


def device_xlsx()->None:
    wb = openpyxl.Workbook()
    ws = wb.active
    if not ws:
        raise Exception("Sheet not found")
    ws.title = "Devices"
    headers = generate_default_device_headers()
    ws.append(headers)

    manufacturer_options = Manufacturer.to_list_str()
    device_role_options = [str(v) for v in DeviceRole]
    manu_col = index_to_col(headers.index('Manufacturer')+1)
    role_col = index_to_col(headers.index('DeviceRole')+1)
    manu_range = CellRange(f"{manu_col}2:{manu_col}300")
    role_range = CellRange(f"{role_col}2:{role_col}300")

    manu_validation = DataValidation(
        type="list",
        formula1=f'"{",".join(manufacturer_options)}"',
        showDropDown=False,
        allow_blank=False,
    )
    manu_validation.add(manu_range)

    role_validation = DataValidation(
        type="list",
        formula1=f'"{",".join(device_role_options)}"',
        showDropDown=False,
        allow_blank=False,
    )
    role_validation.add(role_range)
    ws.add_data_validation(manu_validation)
    ws.add_data_validation(role_validation)

    
    wb.save("devices.xlsx")
