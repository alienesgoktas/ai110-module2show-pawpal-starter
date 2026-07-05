from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task, format_time

owner = Owner("Jordan")

mochi = Pet("Mochi", "dog")
mochi.add_task(Task("Morning walk", 30, "high", time="08:00"))
mochi.add_task(Task("Feeding", 10, "high", time="08:30"))

biscuit = Pet("Biscuit", "cat")
biscuit.add_task(Task("Litter box cleaning", 10, "medium", time="09:00"))
biscuit.add_task(Task("Playtime", 15, "low", time="09:15"))

owner.add_pet(mochi)
owner.add_pet(biscuit)

result = Scheduler().build_schedule_for_owner(owner, available_minutes=60, start_minute=8 * 60)

print(f"Today's Schedule for {owner.name}'s pets")
print("=" * 40)

for scheduled in result.scheduled:
    print(
        f"{format_time(scheduled.start_minute)} - {scheduled.task.title} "
        f"({scheduled.task.duration_minutes} min) [{scheduled.reason}]"
    )

if result.skipped:
    print()
    print("Skipped:")
    for task, reason in result.skipped:
        print(f"  {task.title}: {reason}")

scheduler = Scheduler()

task_owner = {id(t): pet.name for pet in owner.pets for t in pet.tasks}

print()
print("Tasks sorted by time")
print("=" * 40)
for task in scheduler.sort_by_time(owner.all_tasks()):
    print(f"{task.time or '(no time)'} - {task.title} ({task_owner.get(id(task), '?')})")

print()
print("Incomplete tasks (filter by status)")
print("=" * 40)
for task in scheduler.filter_by_status(owner.all_tasks(), completed=False):
    print(f"{task.title}")

print()
print(f"Tasks for {mochi.name} (filter by pet)")
print("=" * 40)
for task in owner.tasks_for_pet(mochi.name):
    print(f"{task.title}")

print()
print("Recurring task demo")
print("=" * 40)
daily_medication = Task(
    "Medication", 5, "high", time="20:00", frequency="daily", due_date=date.today()
)
mochi.add_task(daily_medication)
next_medication = mochi.mark_task_complete(daily_medication)
print(f"Completed '{daily_medication.title}' due {daily_medication.due_date}")
print(f"Next occurrence due {next_medication.due_date}")

print()
print("Conflict detection demo")
print("=" * 40)
mochi.add_task(Task("Vet visit", 20, "medium", time="09:00"))
biscuit.add_task(Task("Brushing", 15, "low", time="09:00"))
conflicts = scheduler.detect_conflicts(owner)
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No conflicts found.")
