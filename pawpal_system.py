from dataclasses import dataclass, field
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
RECURRENCE_INTERVALS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    time: str | None = None
    frequency: str = "once"
    completed: bool = False
    due_date: date | None = None

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Return the next occurrence of this task if it recurs, else None."""
        interval = RECURRENCE_INTERVALS.get(self.frequency)
        if interval is None:
            return None
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=(self.due_date or date.today()) + interval,
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task and, if it recurs, append and return its next occurrence."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.tasks.append(next_task)
        return next_task


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Flatten and return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return the tasks belonging to the pet with the given name, or an empty list."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet.tasks
        return []


@dataclass
class ScheduledTask:
    task: Task
    start_minute: int
    end_minute: int
    reason: str


@dataclass
class ScheduleResult:
    scheduled: list[ScheduledTask]
    skipped: list[tuple[Task, str]]


class Scheduler:
    def build_schedule(
        self, tasks: list[Task], available_minutes: int, start_minute: int = 0
    ) -> ScheduleResult:
        """Order tasks by priority (then duration) and fit as many as possible into the time budget."""
        ordered = sorted(
            tasks, key=lambda t: (PRIORITY_ORDER[t.priority], t.duration_minutes)
        )

        scheduled: list[ScheduledTask] = []
        skipped: list[tuple[Task, str]] = []
        elapsed = 0

        for task in ordered:
            remaining = available_minutes - elapsed
            if task.duration_minutes <= remaining:
                scheduled.append(
                    ScheduledTask(
                        task=task,
                        start_minute=start_minute + elapsed,
                        end_minute=start_minute + elapsed + task.duration_minutes,
                        reason=f"priority: {task.priority}",
                    )
                )
                elapsed += task.duration_minutes
            else:
                skipped.append(
                    (
                        task,
                        f"skipped - not enough remaining time "
                        f"({remaining} min left, needs {task.duration_minutes} min)",
                    )
                )

        return ScheduleResult(scheduled=scheduled, skipped=skipped)

    def build_schedule_for_owner(
        self, owner: Owner, available_minutes: int, start_minute: int = 0
    ) -> ScheduleResult:
        """Collect every task across an owner's pets, then build a schedule from them."""
        return self.build_schedule(owner.all_tasks(), available_minutes, start_minute)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by their HH:MM time string, placing untimed tasks last."""
        return sorted(tasks, key=lambda t: t.time or "24:00")

    def filter_by_status(self, tasks: list[Task], completed: bool) -> list[Task]:
        """Return only the tasks matching the given completion status."""
        return [t for t in tasks if t.completed == completed]

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Return a warning for each clock time shared by two or more of an owner's pending tasks."""
        labels_by_time: dict[str, list[str]] = {}
        for pet in owner.pets:
            for task in pet.tasks:
                if task.time is None or task.completed:
                    continue
                labels_by_time.setdefault(task.time, []).append(f"{pet.name}'s {task.title}")

        return [
            f"Conflict at {time}: {' and '.join(labels)} are scheduled at the same time."
            for time, labels in labels_by_time.items()
            if len(labels) > 1
        ]


def format_time(minute: int) -> str:
    """Convert an absolute minute count into an HH:MM clock string."""
    hours, minutes = divmod(minute, 60)
    hours = hours % 24
    return f"{hours:02d}:{minutes:02d}"
