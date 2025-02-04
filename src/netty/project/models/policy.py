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

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class WebFilter(BaseModel):
    name: str
    urlfilter_table: list["UrlFilterEntry"]
    target_firewall_policy: str


class UrlFilterEntry(BaseModel):
    url: str
    type: Literal["simple", "regex", "wildcard"] = Field(default="simple")
    action: Literal["exempt", "block", "allow", "monitor"]

    @model_validator(mode="after")
    def generate_url_type(self) -> "UrlFilterEntry":
        self.url.strip(" ")
        if self.url.startswith("*."):
            self.type = "wildcard"
            return self
        re_string = ["+", "^", "$", "\\"]
        for item in re_string:
            if item in self.url:
                self.type = "regex"
                return self
        self.type = "simple"
        return self
