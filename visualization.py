# visualization.py
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
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
    Display the weekly schedule using DISCRETE colored grids:
       y-axis = Day 1.. total_days
       x-axis = Hour 0.. hours_per_day-1
       Color = Each task name gets exactly one color
       Colorbar = Task names (categorical)
    """
    if total_days <= 0 or hours_per_day <= 0:
        print("Invalid total_days or hours_per_day.")
        return

    # Collect all task names appearing in the schedule
    all_names: List[str] = []
    for day in range(1, total_days + 1):
        for hour, name in schedule.get(day, []):
            all_names.append(name)

    if not all_names:
        print("Empty schedule. Nothing to visualize.")
        return

    # Stable order so mapping is consistent within this plot
    unique_tasks = sorted(set(all_names))
    task_to_id: Dict[str, int] = {name: i + 1 for i, name in enumerate(unique_tasks)}
    K = len(unique_tasks)

    # Build grid: 0 = empty, 1..K = task id
    grid = np.zeros((total_days, hours_per_day), dtype=int)
    for day in range(1, total_days + 1):
        for hour, name in schedule.get(day, []):
            if 0 <= hour < hours_per_day:
                grid[day - 1, hour] = task_to_id[name]

    # Build a discrete colormap: 0 -> white (empty), 1..K -> categorical colors
    base = plt.get_cmap("tab20")
    colors = ["white"] + [base((i % 20) / 20) for i in range(K)]
    cmap = ListedColormap(colors)

    # Ensure discrete mapping (no interpolation)
    bounds = np.arange(-0.5, K + 1.5, 1)  # [-0.5, 0.5, 1.5, ..., K+0.5]
    norm = BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(10, 4))
    plt.imshow(grid, cmap=cmap, norm=norm, aspect="auto", interpolation="nearest")
    plt.xlabel("Hour of day (0-based)")
    plt.ylabel("Day")
    plt.title("Weekly Schedule (One Color per Task)")

    plt.yticks(
        ticks=range(total_days),
        labels=[f"Day {d}" for d in range(1, total_days + 1)]
    )

    # Colorbar with task names
    cbar = plt.colorbar(ticks=np.arange(1, K + 1))
    cbar.ax.set_yticklabels(unique_tasks)
    cbar.set_label("Task (categorical)")

    plt.tight_layout()
    plt.show()