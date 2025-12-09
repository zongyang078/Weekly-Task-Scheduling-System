# main.py
"""
Main entry point for the Weekly Task Scheduling System.

This program demonstrates our two-component pipeline:
1. Dynamic Programming (DP) for deadline-constrained selection
   of indivisible tasks (splittable == False).
2. Greedy filling for splittable tasks (splittable == True)
   on remaining free time slots.
3. BFS-style time-slot mapping for weekly schedule construction,
   plus basic visualizations (linear timeline + weekly grid).

We run several test cases to show how the system behaves under
different task configurations (normal load, tight deadlines, overload).
"""

from task import Task
from mixed_scheduler import select_and_schedule_mixed_tasks
from bfs_schedule_mapping import build_weekly_schedule_from_blocks
from visualization import plot_linear_timeline, visualize_weekly_schedule


HOURS_PER_DAY = 6
TOTAL_DAYS = 7


def print_selected_tasks(selected_tasks):
    print("\n  Selected Tasks (DP + Greedy):")
    if not selected_tasks:
        print("  -> No tasks selected.")
        return

    for task in selected_tasks:
        splittable_flag = " (splittable)" if task.splittable else ""
        print(f"  - {task.name}{splittable_flag} | Duration: {task.duration} hrs | "
              f"Deadline: Day {task.deadline_day} | Priority: {task.priority}")


def print_weekly_schedule(schedule, total_days):
    print("\n  Weekly Schedule (BFS Time Mapping):")
    for day in range(1, total_days + 1):
        print(f"    Day {day}:")
        if day not in schedule or len(schedule[day]) == 0:
            print("      (No tasks scheduled)")
            continue

        for hour, task_name in schedule[day]:
            print(f"      Hour {hour}: {task_name}")


def run_test_case(case_name: str, tasks):
    print("\n==================================================")
    print(f"Test Case: {case_name}")
    print("==================================================")

    print(f"\n  Total available time: {HOURS_PER_DAY * TOTAL_DAYS} hours "
          f"({TOTAL_DAYS} days × {HOURS_PER_DAY} hours/day)")
    print("  Input Tasks:")
    for t in tasks:
        splittable_flag = " (splittable)" if t.splittable else ""
        print(f"  - {t.name}{splittable_flag} | Duration: {t.duration} hrs | "
              f"Deadline: Day {t.deadline_day} | Priority: {t.priority}")

    # 1. Mixed scheduling: DP for indivisible + greedy for splittable
    selected_tasks, schedule_blocks = select_and_schedule_mixed_tasks(
        tasks, HOURS_PER_DAY, TOTAL_DAYS
    )

    print_selected_tasks(selected_tasks)

    # 2. BFS-style mapping: convert linear timeline → weekly schedule
    schedule = build_weekly_schedule_from_blocks(
        schedule_blocks, HOURS_PER_DAY, TOTAL_DAYS
    )

    print_weekly_schedule(schedule, TOTAL_DAYS)

    # 3. Visualizations
    print("\n  -> Showing linear timeline plot...")
    plot_linear_timeline(schedule_blocks)

    print("  -> Showing weekly schedule grid...")
    visualize_weekly_schedule(schedule, HOURS_PER_DAY, TOTAL_DAYS)

    print("\n")


def main():
    # ---------- Test Case 1: Normal mixed workload ----------
    tasks_case_1 = [
        Task(1, "CS5800 Homework", duration=5, deadline_day=3, priority=10),
        Task(2, "Medical Project Report", duration=6, deadline_day=5, priority=9),
        Task(3, "Resume Update", duration=2, deadline_day=4, priority=8),
        Task(4, "Internship Application", duration=3, deadline_day=7, priority=7),
        Task(5, "Leetcode Practice", duration=4, deadline_day=7, priority=5, splittable=True),
    ]

    # ---------- Test Case 2: Tight deadlines, some almost impossible ----------
    tasks_case_2 = [
        Task(1, "DS5110 Lab Report", duration=5, deadline_day=2, priority=9),
        Task(2, "CS5800 Quiz Preparation", duration=3, deadline_day=2, priority=8),
        Task(3, "Email Professor", duration=1, deadline_day=1, priority=7),
        Task(4, "Short Reading Summary", duration=2, deadline_day=3, priority=6),
        Task(5, "Long-Term Research Reading", duration=8, deadline_day=7, priority=4, splittable=True),
    ]

    # ---------- Test Case 3: Overloaded week (sum of durations > total time) ----------
    # Total available = 7 * 6 = 42 hours
    tasks_case_3 = [
        Task(1, "Big Project Implementation", duration=15, deadline_day=7, priority=10),
        Task(2, "Algorithm Midterm Study", duration=12, deadline_day=5, priority=9),
        Task(3, "Data Science Assignment", duration=10, deadline_day=4, priority=8),
        Task(4, "Side Project Development", duration=10, deadline_day=7, priority=6),
        Task(5, "Gym and Health Routine", duration=7, deadline_day=7, priority=5, splittable=True),
        # Sum of durations = 54 > 42, DP + greedy must drop or trim some tasks
    ]

    print("=== Weekly Task Scheduling System (DP + Greedy + BFS Mapping) ===")

    run_test_case("Normal Mixed Workload", tasks_case_1)
    run_test_case("Tight Deadlines", tasks_case_2)
    run_test_case("Overloaded Week (More Work than Time)", tasks_case_3)


if __name__ == "__main__":
    main()