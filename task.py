# task.py
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    name: str
    duration: int          # total hours needed
    deadline_day: int      # 1..7  (or 1..TOTAL_DAYS)
    priority: int          # importance level
    splittable: bool = False  # True indicate separable tasks (such as doing exercises, reading, etc.)