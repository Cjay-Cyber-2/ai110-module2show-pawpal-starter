# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- **Owner & Pet management** — register an owner and multiple pets with species info
- **Task scheduling** — add care tasks with time, frequency (once/daily/weekly), and completion tracking
- **Sorting by time & priority** — `Scheduler.sort_by_time()` orders tasks chronologically, considering Priority first.
- **Filtering** — filter tasks by pet name (`filter_by_pet`) or completion status (`filter_by_status`)
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags tasks scheduled at the exact same time
- **Data Persistence** — `Owner.save_to_json()` and `load_from_json()` allow the state to persist across runs via `data.json`.
- **Daily/weekly recurrence** — completing a recurring task auto-creates the next occurrence via `Task.mark_complete()`
- **CLI demo with Tables** — `main.py` verifies all backend logic in the terminal before using the Streamlit UI, formatted with `tabulate`.
- **Automated tests** — pytest suite covers sorting, recurrence, conflict detection, JSON serialization, and edge cases

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the CLI demo

```bash
python main.py
```

### Run the Streamlit app

```bash
streamlit run app.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

CLI output from running `python main.py`:

```
=== PawPal+ Today's Schedule ===

+--------+------------+----------+-----------------+----------+-------------+------------+
| Time   | Priority   | Status   | Task            | Pet      | Frequency   | Due Date   |
+========+============+==========+=================+==========+=============+============+
| 08:00  | High       | Pending  | Morning walk    | Buddy    | Daily       | 2026-07-06 |
+--------+------------+----------+-----------------+----------+-------------+------------+
| 09:00  | High       | Pending  | Medication      | Whiskers | Once        | -          |
+--------+------------+----------+-----------------+----------+-------------+------------+
| 09:00  | Low        | Pending  | Grooming        | Whiskers | Once        | -          |
+--------+------------+----------+-----------------+----------+-------------+------------+
| 18:00  | Medium     | Pending  | Evening feeding | Buddy    | Daily       | 2026-07-06 |
+--------+------------+----------+-----------------+----------+-------------+------------+

=== All Tasks Sorted by Time (added out of order) ===

+--------+------------+----------+-----------------+----------+-------------+------------+
| Time   | Priority   | Status   | Task            | Pet      | Frequency   | Due Date   |
+========+============+==========+=================+==========+=============+============+
| 08:00  | High       | Pending  | Morning walk    | Buddy    | Daily       | 2026-07-06 |
+--------+------------+----------+-----------------+----------+-------------+------------+
| 09:00  | High       | Pending  | Medication      | Whiskers | Once        | -          |
+--------+------------+----------+-----------------+----------+-------------+------------+
| 18:00  | Medium     | Pending  | Evening feeding | Buddy    | Daily       | 2026-07-06 |
+--------+------------+----------+-----------------+----------+-------------+------------+
| 09:00  | Low        | Pending  | Grooming        | Whiskers | Once        | -          |
+--------+------------+----------+-----------------+----------+-------------+------------+

=== Conflict Warnings ===
  WARNING: Conflict at 09:00: Medication (Whiskers), Grooming (Whiskers) are all scheduled at the same time.

=== Recurring Task Demo ===
Buddy now has 3 tasks after completing morning walk.
  -> Evening feeding due 2026-07-06 at 18:00
  -> Morning walk due 2026-07-07 at 08:00
```

## 🧪 Testing PawPal+

Run the full test suite:

```bash
python -m pytest
```

The test suite covers:

- **Task completion** — `mark_complete()` sets `completed=True`
- **Task addition** — adding a task increases a pet's task count
- **Sorting correctness** — tasks returned in chronological HH:MM order
- **Recurrence logic** — daily task completion creates a next-day instance
- **Conflict detection** — duplicate times produce a warning message
- **Pet filtering** — only the selected pet's tasks are returned
- **Edge case** — a pet with no tasks yields an empty schedule

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.3, pluggy-1.6.0
collected 7 items

tests/test_pawpal.py::test_task_completion_changes_status PASSED
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED
tests/test_pawpal.py::test_daily_recurrence_creates_next_day_task PASSED
tests/test_pawpal.py::test_conflict_detection_flags_duplicate_times PASSED
tests/test_pawpal.py::test_filter_by_pet_returns_only_matching_tasks PASSED
tests/test_pawpal.py::test_pet_with_no_tasks_returns_empty_schedule PASSED

============================== 7 passed in 0.25s ==============================
```

**Confidence Level:** ★★★★☆ (4/5) — Core scheduling, sorting, filtering, recurrence, and conflict detection are covered by automated tests. Additional edge cases (weekly recurrence, overlapping durations) could be tested with more time.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically considering Priority maps (`High`: 0, `Medium`: 1, `Low`: 2) |
| Filtering | `Scheduler.filter_by_status()`, `Scheduler.filter_by_pet()` | Filter by completion status or pet name (case-insensitive) |
| Conflict handling | `Scheduler.detect_conflicts()` | Lightweight exact-time match detection; returns warning strings instead of crashing |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.complete_task()` | Daily tasks reschedule +1 day; weekly tasks reschedule +7 days using `timedelta` |
| Data Persistence | `Owner.save_to_json()`, `Owner.load_from_json()` | Safely serialize the object graph to `data.json` including date conversions |

## 📸 Demo Walkthrough

1. **Set up the owner** — Enter your name in the Owner section. The app stores your `Owner` object in `st.session_state` so data persists across interactions.

2. **Add pets** — Use the "Add a Pet" form to register one or more pets (e.g., Buddy the dog, Whiskers the cat). Each pet is created as a `Pet` object and added to the owner via `Owner.add_pet()`.

3. **Schedule tasks** — Select a pet, enter a task description, time (HH:MM), and frequency (once/daily/weekly). Submitting the form calls `Pet.add_task()` with a new `Task` instance.

4. **View today's schedule** — The schedule table uses `Scheduler.get_todays_schedule()` to show incomplete tasks sorted by time. Use the pet and status filters to narrow the view. Conflict warnings appear as yellow `st.warning` banners when two tasks share the same time slot.

5. **Complete tasks** — Select a pending task and click "Mark Complete." The scheduler calls `Scheduler.complete_task()`, which marks the task done and auto-creates the next recurring instance for daily/weekly tasks.

Key scheduler behaviors visible in the UI: chronological sorting, pet/status filtering, conflict warnings at duplicate times, and automatic recurrence after completion.

## Project Structure

```
pawpal_system.py      — Core classes: Task, Pet, Owner, Scheduler
main.py               — CLI demo script
app.py                — Streamlit UI
tests/test_pawpal.py  — Automated pytest suite
diagrams/
  uml_draft.mmd       — Initial UML class diagram
  uml_final.mmd       — Final UML matching implemented code
reflection.md         — Design decisions and AI collaboration notes
```

## UML Class Diagram

See `diagrams/uml_final.mmd` for the final Mermaid class diagram showing `Owner`, `Pet`, `Task`, and `Scheduler` relationships.
