from typing import Any
from dataclasses import dataclass

@dataclass
class Task():
    _id:int
    name:str
    description:str
    toughness:int
    tags:"list[str]"

@dataclass
class TaskDetails():
    task_id:int
    content:str
    examples:'list[str]'
    imports:str
    function_name:str
    input_arguments:'list[str]'
    output_type:str

@dataclass
class TaskTest():
    task_id:int
    test_index:int
    input_positional:'list[str]'
    input_dict:'dict[str]'
    output:Any
