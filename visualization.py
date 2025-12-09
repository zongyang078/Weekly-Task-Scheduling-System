# visualization.py
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import numpy as np
from task import Task


def plot_linear_timeline(schedule_blocks: List[Tuple[int, int, Task]]) -> None:
    """
    Draw a Gantt chart on a linear timeline:
        X-axis = Global hour slot
        Y-axis = Task name
    """
    if not schedule_blocks:
        print("No schedule blocks to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))

    for start, end, task in schedule_blocks:
        ax.barh(task.name, end - start, left=start)

    ax.set_xlabel("Hour slot (0-based from week start)")
    ax.set_ylabel("Task")
    ax.set_title("Linear Timeline (DP + Greedy Output)")
    plt.tight_layout()
    plt.show()


def visualize_weekly_schedule(
    schedule: Dict[int, List[Tuple[int, str]]],
    hours_per_day: int,
    total_days: int
) -> None:
    """
    Display the weekly schedule using colored grids:
       y-axis = Day 1.. total_days
       X-axis = Hour 0.. hours_per_day-1
       Color = Different Tasks
    """
    if total_days <= 0 or hours_per_day <= 0:
        print("Invalid total_days or hours_per_day.")
        return

    grid = np.zeros((total_days, hours_per_day))
    task_to_color: Dict[str, int] = {}
    color_id = 1

    for day in range(1, total_days + 1):
        if day not in schedule:
            continue
        for hour, name in schedule[day]:
            if name not in task_to_color:
                task_to_color[name] = color_id
                color_id += 1
            grid[day - 1][hour] = task_to_color[name]

    plt.figure(figsize=(10, 4))
    plt.imshow(grid, cmap="tab20", aspect="auto")
    plt.xlabel("Hour of day (0-based)")
    plt.ylabel("Day")
    plt.title("Weekly Schedule (Color = Task)")
    plt.colorbar(label="Task ID (color)")
    plt.yticks(
        ticks=range(total_days),
        labels=[f"Day {d}" for d in range(1, total_days + 1)]
    )
    plt.tight_layout()
    plt.show()