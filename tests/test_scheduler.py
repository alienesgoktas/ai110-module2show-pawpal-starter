from pawpal_system import Scheduler, Task


def test_orders_by_priority_high_before_low():
    tasks = [
        Task("Feed", 10, "low"),
        Task("Walk", 10, "medium"),
        Task("Meds", 10, "high"),
    ]

    result = Scheduler().build_schedule(tasks, available_minutes=60)

    assert [s.task.title for s in result.scheduled] == ["Meds", "Walk", "Feed"]
    assert result.skipped == []


def test_tie_break_by_shorter_duration():
    tasks = [
        Task("Long walk", 30, "high"),
        Task("Quick check", 5, "high"),
    ]

    result = Scheduler().build_schedule(tasks, available_minutes=60)

    assert [s.task.title for s in result.scheduled] == ["Quick check", "Long walk"]


def test_skips_tasks_when_time_runs_out():
    tasks = [
        Task("Meds", 20, "high"),
        Task("Walk", 20, "medium"),
        Task("Playtime", 20, "low"),
    ]

    result = Scheduler().build_schedule(tasks, available_minutes=40)

    scheduled_titles = [s.task.title for s in result.scheduled]
    skipped_titles = [t.title for t, _ in result.skipped]

    assert scheduled_titles == ["Meds", "Walk"]
    assert skipped_titles == ["Playtime"]
    assert "not enough remaining time" in result.skipped[0][1]


def test_empty_task_list_returns_empty_schedule():
    result = Scheduler().build_schedule([], available_minutes=60)

    assert result.scheduled == []
    assert result.skipped == []


def test_start_times_are_sequential_and_non_overlapping():
    tasks = [
        Task("Meds", 10, "high"),
        Task("Walk", 20, "high"),
    ]

    result = Scheduler().build_schedule(tasks, available_minutes=60, start_minute=480)

    first, second = result.scheduled
    assert first.start_minute == 480
    assert first.end_minute == first.start_minute + first.task.duration_minutes
    assert second.start_minute == first.end_minute
