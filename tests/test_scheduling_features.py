from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_sort_by_time_orders_tasks_and_places_untimed_last():
    tasks = [
        Task("Feeding", 10, "high", time="09:00"),
        Task("Morning walk", 30, "high", time="08:00"),
        Task("Grooming", 20, "low", time=None),
    ]

    ordered = Scheduler().sort_by_time(tasks)

    assert [t.title for t in ordered] == ["Morning walk", "Feeding", "Grooming"]


def test_filter_by_status_returns_only_matching_tasks():
    done = Task("Feeding", 10, "high", completed=True)
    pending = Task("Morning walk", 30, "high", completed=False)

    incomplete = Scheduler().filter_by_status([done, pending], completed=False)
    complete = Scheduler().filter_by_status([done, pending], completed=True)

    assert incomplete == [pending]
    assert complete == [done]


def test_tasks_for_pet_returns_only_that_pets_tasks():
    mochi = Pet("Mochi", "dog")
    mochi.add_task(Task("Morning walk", 30, "high"))
    biscuit = Pet("Biscuit", "cat")
    biscuit.add_task(Task("Litter box", 10, "medium"))

    owner = Owner("Jordan")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    assert owner.tasks_for_pet("Mochi") == mochi.tasks
    assert owner.tasks_for_pet("Biscuit") == biscuit.tasks
    assert owner.tasks_for_pet("Unknown") == []


def test_mark_task_complete_creates_next_daily_occurrence_one_day_later():
    pet = Pet("Mochi", "dog")
    today = date(2026, 7, 5)
    task = Task("Feeding", 10, "high", frequency="daily", due_date=today)
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task in pet.tasks


def test_mark_task_complete_creates_next_weekly_occurrence_seven_days_later():
    pet = Pet("Mochi", "dog")
    today = date(2026, 7, 5)
    task = Task("Grooming", 30, "low", frequency="weekly", due_date=today)
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_mark_task_complete_does_not_recur_for_once_frequency():
    pet = Pet("Mochi", "dog")
    task = Task("Vet visit", 60, "high", frequency="once")
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert task.completed is True
    assert next_task is None
    assert len(pet.tasks) == 1


def test_detect_conflicts_flags_same_time_tasks_across_pets():
    mochi = Pet("Mochi", "dog")
    mochi.add_task(Task("Morning walk", 30, "high", time="08:00"))
    biscuit = Pet("Biscuit", "cat")
    biscuit.add_task(Task("Feeding", 10, "high", time="08:00"))

    owner = Owner("Jordan")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Mochi's Morning walk" in warnings[0]
    assert "Biscuit's Feeding" in warnings[0]


def test_detect_conflicts_returns_empty_when_no_time_overlap():
    mochi = Pet("Mochi", "dog")
    mochi.add_task(Task("Morning walk", 30, "high", time="08:00"))
    biscuit = Pet("Biscuit", "cat")
    biscuit.add_task(Task("Feeding", 10, "high", time="09:00"))

    owner = Owner("Jordan")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    assert Scheduler().detect_conflicts(owner) == []
