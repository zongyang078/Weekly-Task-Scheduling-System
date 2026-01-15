# Weekly Task Scheduling System (Dynamic Programming + Greedy)

## Overview
This project designs and implements an automated **weekly task scheduling system** that generates feasible and efficient schedules under time and deadline constraints.

The system combines **Dynamic Programming (DP)** for globally optimal task selection with a **Greedy scheduling strategy** for local time-slot filling. It is motivated by real-world scheduling challenges faced by graduate students managing coursework, projects, career preparation, and personal commitments.

This project was completed as the final project for **CS 5800: Algorithms**.


## Problem Statement
Graduate students often juggle multiple tasks with:
- Limited weekly time
- Hard deadlines
- Different priorities
- Varying execution constraints (splittable vs. indivisible tasks)

Existing tools such as calendars or to-do lists provide static reminders but do not generate **optimized schedules**.

The goal of this project is to answer:
> How can we automatically generate a **deadline-aware, priority-maximizing weekly schedule** that efficiently fills available time while avoiding infeasible plans?


## Task Model
Each task is represented with the following attributes:
- **Duration** (in hours)
- **Deadline** (day 1–7 of the week)
- **Priority value**
- **Splittable flag** (whether the task can be divided into smaller units)

System constraints:
- Weekly time budget: **7 days × 6 hours = 42 hours**
- Tasks may span multiple days
- Indivisible tasks must be scheduled as continuous blocks


## Algorithmic Approach

### Stage 1: Dynamic Programming (Global Optimization)
Dynamic Programming is used to select the optimal subset of tasks that:
- Respects deadline constraints
- Fits within the weekly time limit
- Maximizes total priority

We define:
dp[i][t] = maximum priority achievable using the first i tasks within t hours
This formulation is analogous to **knapsack / weighted interval scheduling** under time constraints.  
The DP stage outputs an optimal allocation of time blocks for indivisible tasks.

**Time Complexity**:  
- DP runs in approximately **O(N × T)**, where:
  - N = number of tasks
  - T = total available weekly hours


### Stage 2: Greedy Scheduling (Local Feasibility)
After DP assigns time to indivisible tasks, a Greedy algorithm fills remaining free slots using **splittable tasks**.

Greedy strategy:
- Sort splittable tasks by:
  1. Earlier deadline
  2. Higher priority density (priority / duration)
- Assign remaining time slots before each task’s deadline

This step improves time utilization and reduces idle gaps while maintaining feasibility.


## Evaluation Scenarios
The system is tested under three representative scenarios:

1. **Normal workload**
   - All tasks are successfully scheduled
   - DP places indivisible tasks optimally
   - Greedy fills remaining slots with flexible tasks

2. **Tight deadlines**
   - Early-deadline tasks are prioritized
   - Long-term or flexible tasks are deferred
   - System shows strong deadline sensitivity

3. **Overloaded week (> 42 hours)**
   - DP selectively drops low-priority tasks
   - High-value tasks are preserved
   - Splittable tasks are partially scheduled where possible

Visualizations (Gantt charts and weekly heatmaps) are used to compare schedules and validate algorithm behavior.


## Key Results
- DP guarantees optimal selection for indivisible tasks under constraints
- Greedy efficiently utilizes leftover time for flexible tasks
- The combined approach:
  - Satisfies deadlines
  - Maximizes total priority
  - Improves weekly time utilization

The system successfully demonstrates that **global optimization + local heuristics** is effective for practical scheduling problems.


## Limitations
- DP becomes expensive when the time horizon T is very large
- Greedy scheduling is not globally optimal for splittable tasks
- Task dependencies (prerequisites) are not modeled
- Fixed task durations; no modeling of fatigue or productivity variation


## Future Work
- Add task dependency graphs (DAG-based scheduling)
- Model variable productivity across time of day
- Replace Greedy with ILP for globally optimal soft-task placement
- Export schedules to calendar systems (e.g., Google Calendar)
- Develop a lightweight GUI or mobile interface


## Project Structure
├── src/            # DP and Greedy scheduling logic
├── data/           # Synthetic and real task datasets (JSON)
├── figures/        # Gantt charts and heatmaps
├── slides/         # Final presentation slides
└── README.md


## Tools & Technologies
- Python
- Dynamic Programming
- Greedy Algorithms
- Data structures and algorithm analysis
- Matplotlib (visualization)


## Contributors
- **Zongyang Li** – Dynamic Programming design, optimization logic, result analysis
- **Zhenyu Wang** – Greedy scheduling, task modeling, test case construction


## Course Context
This project was developed for **CS 5800: Algorithms** and focuses on algorithmic modeling, correctness, and complexity analysis rather than UI or machine learning.
