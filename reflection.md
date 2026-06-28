# PawPal+ Project Reflection

## System Design

Three core actions a user should be able to perform with PawPal+:

1. **Add a pet** — Register one or more pets under an owner so the system knows who needs care.
2. **Schedule a task** — Assign care activities (walks, feeding, medication) with a specific time and frequency.
3. **View today's schedule** — See all pending tasks sorted by time, with conflict warnings when two tasks overlap.

---

## 1. System Design

**a. Initial design**

I designed four core classes based on the pet care domain:

- **Task** — Represents a single care activity with description, time (HH:MM), frequency (once/daily/weekly), completion status, and optional due date. The `mark_complete()` method handles marking done and generating recurring follow-ups.
- **Pet** — Stores a pet's name, species, and a list of tasks. Provides `add_task()` and `get_tasks()` for task management.
- **Owner** — Manages multiple pets and exposes `get_all_tasks()` to gather tasks across the household.
- **Scheduler** — The "brain" that retrieves tasks from the owner, sorts them by time, filters by pet or status, detects time conflicts, and handles task completion with recurrence.

The UML diagram (`diagrams/uml_draft.mmd`) shows Owner owns Pets, Pets have Tasks, and Scheduler manages the Owner's data.

**b. Design changes**

After AI review of the initial skeleton, I kept the four-class design but refined how recurrence works. Originally I considered putting recurrence logic entirely in the Scheduler, but I moved it into `Task.mark_complete()` so the Task knows how to create its own next instance. This keeps the Scheduler focused on orchestration rather than task-level details. The Scheduler's `complete_task()` method now delegates to `Task.mark_complete()` and appends the returned instance to the pet's task list.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers:

- **Time** — Tasks are sorted chronologically by HH:MM string for daily planning.
- **Completion status** — Only incomplete tasks appear in today's schedule.
- **Due date** — Recurring tasks with future due dates are excluded until their date arrives.
- **Pet identity** — Tasks can be filtered to a single pet for focused views.

Time ordering mattered most because pet owners need a clear chronological view of their day. Completion status is second because completed tasks should not clutter the active schedule.

**b. Tradeoffs**

The scheduler only checks for **exact time matches** (e.g., two tasks both at 09:00) rather than detecting overlapping durations (e.g., a 30-minute walk starting at 08:00 conflicting with a 09:00 feeding). This is reasonable for PawPal+ because tasks are modeled as point-in-time events without duration fields in the core design. A full overlap check would require adding duration attributes and more complex interval logic, which is beyond the scope of this project. The lightweight approach gives useful warnings without over-engineering.

---

## 3. AI Collaboration

**a. How you used AI**

I used Cursor Agent (Auto) as my AI coding assistant throughout all six phases:

- **Phase 1 (Design):** Asked AI to generate a Mermaid.js UML class diagram from brainstormed attributes and methods, then translate it into Python dataclass skeletons.
- **Phase 2 (Implementation):** Used agent mode to flesh out all four classes, create `main.py`, and draft initial pytest tests.
- **Phase 3 (UI Integration):** Asked AI how `st.session_state` works and wired `app.py` to the logic layer.
- **Phase 4 (Algorithms):** Used AI to implement sorting with lambda keys, filtering methods, recurrence with `timedelta`, and lightweight conflict detection.
- **Phase 5 (Testing):** Asked AI for edge cases to test (empty pet, duplicate times, recurrence) and generated the expanded test suite.
- **Phase 6 (Polish):** AI helped draft README sections, update the final UML, and complete this reflection.

The most effective features were **agent mode for multi-file edits** (simultaneously updating `pawpal_system.py`, `main.py`, and tests) and **code review prompts** ("Does this skeleton have missing relationships?").

**b. Judgment and verification**

One AI suggestion I modified was to add a separate `Schedule` dataclass to hold the daily plan output. I rejected this because it added an unnecessary layer — the assignment's four-class design (Owner, Pet, Task, Scheduler) was sufficient. The Scheduler can return sorted/filtered task lists directly without wrapping them in another object. Keeping the design flat made the code easier to test and connect to Streamlit.

I verified AI-generated code by running `python main.py` after each phase and checking that `python -m pytest` passed with green results. When the AI suggested a complex conflict detection algorithm using interval trees, I chose the simpler exact-time-match approach because it was easier to read, test, and explain.

**Separate chat sessions:** Using separate sessions for algorithmic planning (Phase 4) versus core implementation (Phase 2) helped keep context focused. The algorithm session could reference sorting/filtering without being cluttered by UI wiring details.

**Lead architect takeaway:** AI is most valuable for scaffolding and boilerplate, but the human architect must decide class boundaries, reject over-engineering, and verify behavior with tests. I treated AI output as a first draft, not a final design.

---

## 4. Testing and Verification

**a. What you tested**

- Task completion status change (`mark_complete()`)
- Task count increase when adding to a pet
- Chronological sorting by HH:MM time
- Daily recurrence creating a next-day task
- Conflict detection for duplicate times
- Pet-name filtering
- Edge case: pet with no tasks returns empty schedule

These tests cover the happy paths (normal scheduling flow) and key edge cases (empty data, duplicate times, recurrence).

**b. Confidence**

Confidence level: **4 out of 5 stars.**

The core scheduling pipeline works and is verified by 7 passing tests. If I had more time, I would test weekly recurrence end-to-end, tasks with past due dates, and case sensitivity edge cases in pet name lookups.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the CLI-first workflow. Building and verifying `pawpal_system.py` through `main.py` before touching Streamlit meant the UI integration in Phase 3 was straightforward — the backend was already proven.

**b. What you would improve**

If I had another iteration, I would add task duration and implement true interval-based conflict detection. I would also add JSON persistence so pets and tasks survive app restarts.

**c. Key takeaway**

The most important lesson is that good system design — clear class responsibilities, a CLI verification path, and targeted tests — makes AI-assisted development much more reliable. AI can generate code quickly, but the architect's job is to define boundaries, verify output, and reject unnecessary complexity.
