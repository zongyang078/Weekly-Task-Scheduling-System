# dp_task_selection.py
from typing import List, Tuple
from task import Task


def select_tasks_with_deadlines_dp(
    tasks: List[Task],
    hours_per_day: int,
    total_days: int
) -> Tuple[List[Task], List[Tuple[int, int, Task]]]:
    """
    Dynamic Programming for deadline-constrained task selection.

    Returns:
      selected_tasks: list of tasks chosen by DP (ordered by deadline)
      schedule_blocks: list of (start_slot, end_slot, task) representing
                       the linear schedule on [0, T)
    """
    # 1. Sort tasks by increasing deadline
    sorted_tasks = sorted(tasks, key=lambda t: t.deadline_day)
    n = len(sorted_tasks)
    T = hours_per_day * total_days  # total available hours in the week

    # 2. DP table: dp[i][t] = max priority using first i tasks with exactly t hours
    dp = [[-1] * (T + 1) for _ in range(n + 1)]
    dp[0][0] = 0   # zero tasks, zero hours = 0 priority

    for i in range(1, n + 1):
        task = sorted_tasks[i - 1]
        dur = task.duration
        # 防御性写法：deadline_slot 不超过 T
        deadline_slot = min(task.deadline_day * hours_per_day, T)

        for t in range(T + 1):
            # Option 1: do not choose the task
            if dp[i - 1][t] != -1:
                if dp[i][t] < dp[i - 1][t]:
                    dp[i][t] = dp[i - 1][t]

            # Option 2: choose the task (must finish before its deadline)
            if t >= dur and dp[i - 1][t - dur] != -1:
                if t <= deadline_slot:
                    candidate = dp[i - 1][t - dur] + task.priority
                    if candidate > dp[i][t]:
                        dp[i][t] = candidate

    # 3. Find best t (max priority)
    best_t = 0
    best_val = -1
    for t in range(T + 1):
        if dp[n][t] > best_val:
            best_val = dp[n][t]
            best_t = t

    # 4. Backtrack to recover selected tasks
    selected_flags = [False] * n
    t = best_t

    for i in range(n, 0, -1):
        if dp[i][t] == dp[i - 1][t]:
            continue
        task = sorted_tasks[i - 1]
        dur = task.duration
        if t >= dur and dp[i][t] == dp[i - 1][t - dur] + task.priority:
            selected_flags[i - 1] = True
            t -= dur

    selected_tasks = [sorted_tasks[i] for i in range(n) if selected_flags[i]]

    # 5. Build linear schedule (continuous time blocks)
    schedule_blocks: List[Tuple[int, int, Task]] = []
    current_time = 0
    for i, task in enumerate(sorted_tasks):
        if selected_flags[i]:
            start = current_time
            end = current_time + task.duration
            schedule_blocks.append((start, end, task))
            current_time = end

    return selected_tasks, schedule_blocks