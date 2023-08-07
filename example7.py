#!/usr/bin/env python3
import scripthelper
from dataclasses import dataclass

scripthelper.bootstrap()


@dataclass
class Item:
    name: str
    value: int


something = {
    "string": "value1",
    "bool": True,
    "none": None,
    "integer": 1234,
    "item": Item("name", 999),
}

scripthelper.pp(something)
