"""CLI demo script for PawPal+ — verifies backend logic in the terminal."""

from datetime import date
from tabulate import tabulate

from pawpal_system import Owner, Pet, Scheduler, Task


def format_schedule(tasks: list[tuple[str, Task]]) -> str:
    """Format a list of (pet_name, task) pairs for readable terminal output using tabulate."""
    if not tasks:
        return "  (no tasks scheduled)"
    
    table_data = []
    for pet_name, task in tasks:
        status = "Done" if task.completed else "Pending"
        due = str(task.due_date) if task.due_date else "-"
        table_data.append([
            task.time,
            task.priority,
            status,
            task.description,
            pet_name,
            task.frequency.capitalize(),
            due
        ])
        
    headers = ["Time", "Priority", "Status", "Task", "Pet", "Frequency", "Due Date"]
    return "\n" + tabulate(table_data, headers=headers, tablefmt="grid")


def main() -> None:
    owner = Owner(name="Chijioke")
    buddy = Pet(name="Buddy", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    buddy.add_task(
        Task(
            description="Morning walk",
            time="08:00",
            frequency="daily",
            due_date=date.today(),
            priority="High"
        )
    )
    buddy.add_task(
        Task(
            description="Evening feeding",
            time="18:00",
            frequency="daily",
            due_date=date.today(),
            priority="Medium"
        )
    )
    whiskers.add_task(Task(description="Medication", time="09:00", frequency="once", priority="High"))
    whiskers.add_task(Task(description="Grooming", time="09:00", frequency="once", priority="Low"))

    scheduler = Scheduler(owner)

    print("=== PawPal+ Today's Schedule ===")
    print(format_schedule(scheduler.get_todays_schedule()))

    print("\n=== All Tasks Sorted by Time (added out of order) ===")
    all_tasks = scheduler.get_all_tasks()
    print(format_schedule(scheduler.sort_by_time(all_tasks)))

    print("\n=== Incomplete Tasks Only ===")
    incomplete = scheduler.filter_by_status(all_tasks, completed=False)
    print(format_schedule(scheduler.sort_by_time(incomplete)))

    print("\n=== Buddy's Tasks Only ===")
    print(format_schedule(scheduler.filter_by_pet(all_tasks, "Buddy")))

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("\n=== Conflict Warnings ===")
        for warning in conflicts:
            print(f"  WARNING: {warning}")

    print("\n=== Recurring Task Demo ===")
    scheduler.complete_task("Buddy", 0)
    print(f"Buddy now has {len(buddy.tasks)} tasks after completing morning walk.")
    new_pending = [t for t in buddy.tasks if not t.completed]
    for task in new_pending:
        print(f"  -> {task.description} due {task.due_date} at {task.time}")


if __name__ == "__main__":
    main()
