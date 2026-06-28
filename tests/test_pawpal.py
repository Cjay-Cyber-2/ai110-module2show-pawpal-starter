"""Automated tests for the PawPal+ system."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task(description="Morning walk", time="08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Buddy", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feed", time="07:00"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(description="Walk", time="08:00"))
    assert len(pet.tasks) == 2


def test_sort_by_time_returns_chronological_order():
    """Verify tasks are returned in chronological order."""
    owner = Owner(name="Test")
    pet = Pet(name="Max", species="dog")
    pet.add_task(Task(description="Evening", time="18:00"))
    pet.add_task(Task(description="Morning", time="08:00"))
    pet.add_task(Task(description="Afternoon", time="14:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    times = [task.time for _, task in sorted_tasks]
    assert times == ["08:00", "14:00", "18:00"]


def test_daily_recurrence_creates_next_day_task():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    owner = Owner(name="Test")
    pet = Pet(name="Luna", species="cat")
    today = date.today()
    pet.add_task(
        Task(
            description="Medication",
            time="09:00",
            frequency="daily",
            due_date=today,
        )
    )
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert len(pet.tasks) == 1
    scheduler.complete_task("Luna", 0)
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True

    new_task = pet.tasks[1]
    assert new_task.completed is False
    assert new_task.frequency == "daily"
    assert new_task.due_date == today + timedelta(days=1)


def test_conflict_detection_flags_duplicate_times():
    """Verify that the Scheduler flags duplicate times."""
    owner = Owner(name="Test")
    buddy = Pet(name="Buddy", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    buddy.add_task(Task(description="Walk", time="09:00"))
    whiskers.add_task(Task(description="Grooming", time="09:00"))
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "09:00" in warnings[0]
    assert "Conflict" in warnings[0]


def test_filter_by_pet_returns_only_matching_tasks():
    """Verify pet-name filtering returns only that pet's tasks."""
    owner = Owner(name="Test")
    buddy = Pet(name="Buddy", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    buddy.add_task(Task(description="Walk", time="08:00"))
    whiskers.add_task(Task(description="Feed", time="08:00"))
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    scheduler = Scheduler(owner)
    buddy_tasks = scheduler.filter_by_pet(owner.get_all_tasks(), "Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0][0] == "Buddy"


def test_pet_with_no_tasks_returns_empty_schedule():
    """Edge case: a pet with no tasks should produce an empty schedule."""
    owner = Owner(name="Test")
    owner.add_pet(Pet(name="Empty", species="dog"))
    scheduler = Scheduler(owner)
    assert scheduler.get_todays_schedule() == []
