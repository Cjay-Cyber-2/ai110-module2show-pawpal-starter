# AI Interactions Log

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**
Implement JSON Data Persistence (Challenge 2), Priority Scheduling (Challenge 3), and Output Formatting (Challenge 4). The agent had to add a `priority` attribute to tasks, modify sorting logic, create a `data.json` saving mechanism for Streamlit state persistence, and implement `tabulate` for CLI output.

**What did the agent do?**
1. Added a `priority` attribute with a default to `Task` in `pawpal_system.py`.
2. Implemented `save_to_json` and `load_from_json` in the `Owner` class using custom serialization for `datetime.date`.
3. Updated `Scheduler.sort_by_time` to use a priority map first, then time string.
4. Integrated saving to `app.py` when forms were submitted.
5. Formatted the output in `main.py` into professional grid tables using `tabulate`.

**What did you have to verify or fix manually?**
I noticed that standard JSON serialization fails on `datetime.date` objects. The agent handled it nicely with a custom `default_serializer` function during `json.dump`, and `date.fromisoformat` on load. I also had to make sure the agent removed Windows console-incompatible emojis when printing tabulate tables in `main.py` so it didn't throw a UnicodeEncodeError.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Gemini | Claude |
| **Prompt** | "How can I serialize a dataclass with datetime.date fields to JSON in Python?" | "How can I serialize a dataclass with datetime.date fields to JSON in Python?" |
| **Response summary** | Suggested using `json.dump` with a custom `default` serialization lambda that calls `.isoformat()` on dates. | Suggested using a robust validation library like `marshmallow` or `pydantic`. |
| **What was useful** | Very straightforward, native solution. No external dependencies needed. | Good structure, handles edge cases better, excellent for scaling complex models. |
| **Problems noticed** | Manual deserialization is slightly tedious for deeply nested fields. | `marshmallow` is overkill for a small CLI/Streamlit script and introduces extra packages. |
| **Decision** | I chose Option A (Gemini) because keeping external dependencies low is cleaner for this project context. | |

**Which approach did you use in your final implementation and why?**
I went with the native `json` module approach with a custom `default_serializer` that converts dates to ISO strings, as it keeps the core logic decoupled from heavy external schemas while being easy to debug.
