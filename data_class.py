from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    id: int
    name: str
    duration: int          # total hours needed
    deadline_day: int      # 1-7
    priority: int          # larger = more important
    dependencies: List[int]
