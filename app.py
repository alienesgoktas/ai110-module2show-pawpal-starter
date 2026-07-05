import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task, format_time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner = st.session_state.owner
owner.name = owner_name

st.subheader("Pets")
col_pet_name, col_species = st.columns(2)
with col_pet_name:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_species:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species))

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"Pet": p.name, "Species": p.species, "Tasks": len(p.tasks)}
            for p in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Tasks")

if not owner.pets:
    st.info("Add a pet first.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        for pet in owner.pets:
            if pet.name == selected_pet_name:
                pet.add_task(
                    Task(title=task_title, duration_minutes=int(duration), priority=priority)
                )
                break

    for pet in owner.pets:
        st.write(f"Tasks for {pet.name}:")
        if pet.tasks:
            st.table(
                [
                    {
                        "Title": t.title,
                        "Duration (min)": t.duration_minutes,
                        "Priority": t.priority,
                    }
                    for t in pet.tasks
                ]
            )
        else:
            st.caption("No tasks yet.")

st.divider()

st.subheader("Build Schedule")

col_time, col_start = st.columns(2)
with col_time:
    available_minutes = st.number_input(
        "Available time today (minutes)", min_value=1, max_value=1440, value=120
    )
with col_start:
    start_hour = st.number_input("Start hour (0-23)", min_value=0, max_value=23, value=8)

if st.button("Generate schedule"):
    if not owner.pets or not any(pet.tasks for pet in owner.pets):
        st.info("Add at least one pet with a task before generating a schedule.")
    else:
        task_owner = {id(t): pet.name for pet in owner.pets for t in pet.tasks}

        result = Scheduler().build_schedule_for_owner(
            owner, available_minutes=int(available_minutes), start_minute=int(start_hour) * 60
        )

        if result.scheduled:
            st.write("Scheduled plan:")
            st.table(
                [
                    {
                        "Time": format_time(s.start_minute),
                        "Pet": task_owner.get(id(s.task), ""),
                        "Task": s.task.title,
                        "Duration (min)": s.task.duration_minutes,
                        "Priority": s.task.priority,
                        "Why": s.reason,
                    }
                    for s in result.scheduled
                ]
            )
        else:
            st.info("No tasks fit in the available time.")

        if result.skipped:
            st.write("Skipped tasks:")
            st.table(
                [
                    {
                        "Pet": task_owner.get(id(task), ""),
                        "Task": task.title,
                        "Priority": task.priority,
                        "Reason": reason,
                    }
                    for task, reason in result.skipped
                ]
            )
