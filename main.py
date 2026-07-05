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
