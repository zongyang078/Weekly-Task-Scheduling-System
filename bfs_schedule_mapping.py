# bfs_schedule_mapping.py
from collections import defaultdict
from typing import Dict, List, Tuple
from task import Task


def build_weekly_schedule_from_blocks(
    schedule_blocks: List[Tuple[int, int, Task]],
    hours_per_day: int,
    total_days: int
) -> Dict[int, List[Tuple[int, str]]]:
    """
    Converts linear time blocks into a weekly schedule.

    Returns:
      schedule: dict mapping day (1-based) -> list of (hour_in_day, task_name)
    """
    schedule: Dict[int, List[Tuple[int, str]]] = defaultdict(list)

    for (start, end, task) in schedule_blocks:
        for slot in range(start, end):
            day = slot // hours_per_day + 1          # 1-based day
            hour_in_day = slot % hours_per_day       # 0..hours_per_day-1

            if day <= total_days:
                schedule[day].append((hour_in_day, task.name))

    # Sort hours within each day
    for day in schedule:
        schedule[day].sort(key=lambda x: x[0])

    return schedule