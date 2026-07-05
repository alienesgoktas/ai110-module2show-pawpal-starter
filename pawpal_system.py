from dataclasses import dataclass, field

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    time: str | None = None
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


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


def format_time(minute: int) -> str:
    """Convert an absolute minute count into an HH:MM clock string."""
    hours, minutes = divmod(minute, 60)
    hours = hours % 24
    return f"{hours:02d}:{minutes:02d}"
