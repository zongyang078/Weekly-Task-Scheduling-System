# mixed_scheduler.py
from typing import List, Tuple, Optional
from task import Task
from dp_task_selection import select_tasks_with_deadlines_dp


def select_and_schedule_mixed_tasks(
    tasks: List[Task],
    hours_per_day: int,
    total_days: int
) -> Tuple[List[Task], List[Tuple[int, int, Task]]]:
    """
    Mixed scheduling:
      - Indivisible tasks (splittable == False): selected and scheduled by DP.
      - Splittable tasks (splittable == True): filled greedily into remaining slots.

    Returns:
      selected_tasks: all tasks that actually got some time on the timeline
      schedule_blocks: linear time blocks (start_slot, end_slot, task)
                       on [0, T), combining DP + greedy.
    """
    T = hours_per_day * total_days

    # 1. Split tasks into indivisible and splittable
    indivisible_tasks = [t for t in tasks if not t.splittable]
    splittable_tasks = [t for t in tasks if t.splittable]

    # 2. Use original DP on indivisible tasks
    selected_indivisible, blocks_indivisible = select_tasks_with_deadlines_dp(
        indivisible_tasks, hours_per_day, total_days
    )

    # 3. Mark occupied slots on linear time axis
    slot_owner: List[Optional[Task]] = [None] * T
    for start, end, task in blocks_indivisible:
        for s in range(start, min(end, T)):
            slot_owner[s] = task

    # 4. Greedy fill splittable tasks into free slots
    def density(t: Task) -> float:
        return t.priority / max(1, t.duration)

    splittable_tasks_sorted = sorted(
        splittable_tasks,
        key=lambda t: (t.deadline_day, -density(t))
    )

    used_splittable: List[Task] = []

    for task in splittable_tasks_sorted:
        remaining = task.duration
        deadline_slot = min(task.deadline_day * hours_per_day, T)

        for s in range(deadline_slot):
            if remaining == 0:
                break
            if slot_owner[s] is None:
                slot_owner[s] = task
                remaining -= 1

        if remaining < task.duration and task not in used_splittable:
            used_splittable.append(task)

    # 5. Compress slot_owner back into schedule_blocks
    blocks_mixed: List[Tuple[int, int, Task]] = []
    s = 0
    while s < T:
        if slot_owner[s] is None:
            s += 1
            continue
        task = slot_owner[s]
        e = s + 1
        while e < T and slot_owner[e] is task:
            e += 1
        blocks_mixed.append((s, e, task))
        s = e

    # 6. Collect all actually used tasks
    selected_tasks = list(selected_indivisible) + used_splittable

    return selected_tasks, blocks_mixed