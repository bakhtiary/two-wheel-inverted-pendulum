from dataclasses import dataclass


@dataclass
class Capability:
    id: int
    cur_value: int
    increment: int
    print_name: str
