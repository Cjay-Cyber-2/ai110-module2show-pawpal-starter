"""PawPal+ logic layer — core classes for pet care task management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care activity."""

    description: str
    time: str
    frequency: str = "once"
    completed: bool = False
    due_date: Optional[date] = None

    def mark_complete(self) -> Optional[Task]:
        """Mark this task complete and return a recurring follow-up if applicable."""
        self.completed = True
        if self.frequency == "daily":
            next_due = (self.due_date or date.today()) + timedelta(days=1)
            return Task(
                description=self.description,
                time=self.time,
                frequency="daily",
                completed=False,
                due_date=next_due,
            )
        if self.frequency == "weekly":
            next_due = (self.due_date or date.today()) + timedelta(days=7)
            return Task(
                description=self.description,
                time=self.time,
                frequency="weekly",
                completed=False,
                due_date=next_due,
            )
        return None


@dataclass
class Pet:
    """Stores pet details and a list of care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's schedule."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name (case-insensitive)."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> list[tuple[str, Task]]:
        """Return all tasks across pets as (pet_name, task) pairs."""
        return [(pet.name, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes, and manages tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_all_tasks(self) -> list[tuple[str, Task]]:
        """Retrieve every task from all of the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list[tuple[str, Task]]) -> list[tuple[str, Task]]:
        """Sort tasks chronologically by their HH:MM time string."""
        return sorted(tasks, key=lambda item: item[1].time)

    def filter_by_status(
        self, tasks: list[tuple[str, Task]], completed: bool
    ) -> list[tuple[str, Task]]:
        """Filter tasks by completion status."""
        return [(pet, task) for pet, task in tasks if task.completed == completed]

    def filter_by_pet(
        self, tasks: list[tuple[str, Task]], pet_name: str
    ) -> list[tuple[str, Task]]:
        """Filter tasks belonging to a specific pet."""
        return [
            (pet, task) for pet, task in tasks if pet.lower() == pet_name.lower()
        ]

    def get_todays_schedule(self) -> list[tuple[str, Task]]:
        """Return today's incomplete tasks sorted by time."""
        today = date.today()
        active = [
            (pet, task)
            for pet, task in self.get_all_tasks()
            if not task.completed
            and (task.due_date is None or task.due_date <= today)
        ]
        return self.sort_by_time(active)

    def detect_conflicts(
        self, tasks: Optional[list[tuple[str, Task]]] = None
    ) -> list[str]:
        """Detect tasks scheduled at the exact same time and return warnings."""
        if tasks is None:
            tasks = self.get_all_tasks()

        time_map: dict[str, list[str]] = {}
        for pet_name, task in tasks:
            if task.completed:
                continue
            label = f"{task.description} ({pet_name})"
            time_map.setdefault(task.time, []).append(label)

        warnings: list[str] = []
        for time_slot, entries in time_map.items():
            if len(entries) > 1:
                joined = ", ".join(entries)
                warnings.append(
                    f"Conflict at {time_slot}: {joined} are all scheduled at the same time."
                )
        return warnings

    def complete_task(self, pet_name: str, task_index: int) -> None:
        """Mark a task complete and auto-create the next recurring instance."""
        pet = self.owner.get_pet(pet_name)
        if pet is None or task_index >= len(pet.tasks):
            return
        next_task = pet.tasks[task_index].mark_complete()
        if next_task is not None:
            pet.add_task(next_task)
