"""Streamlit UI for PawPal+ — connects to the pawpal_system logic layer."""

from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.caption("Smart pet care management — schedule, track, and prioritize daily routines.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Chijioke")

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

col_owner, col_pet = st.columns(2)

with col_owner:
    st.subheader("Owner")
    new_owner_name = st.text_input("Owner name", value=owner.name)
    if new_owner_name != owner.name:
        owner.name = new_owner_name

with col_pet:
    st.subheader("Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["dog", "cat", "bird", "other"])
        if st.form_submit_button("Add Pet"):
            if pet_name.strip():
                owner.add_pet(Pet(name=pet_name.strip(), species=species))
                st.success(f"Added {pet_name}!")
            else:
                st.error("Please enter a pet name.")

st.divider()

st.subheader("Schedule a Task")
if not owner.pets:
    st.info("Add at least one pet before scheduling tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_options = {pet.name: pet for pet in owner.pets}
        selected_pet = st.selectbox("Pet", list(pet_options.keys()))
        task_desc = st.text_input("Task description", placeholder="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add Task"):
            if task_desc.strip():
                pet_options[selected_pet].add_task(
                    Task(
                        description=task_desc.strip(),
                        time=task_time,
                        frequency=frequency,
                        due_date=date.today() if frequency != "once" else None,
                    )
                )
                st.success(f"Scheduled '{task_desc}' for {selected_pet} at {task_time}.")
            else:
                st.error("Please enter a task description.")

st.divider()

st.subheader("Today's Schedule")
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    pet_filter = st.selectbox(
        "Filter by pet",
        ["All pets"] + [pet.name for pet in owner.pets],
    )
with filter_col2:
    status_filter = st.selectbox(
        "Filter by status",
        ["All", "Pending only", "Completed only"],
    )

schedule = scheduler.get_todays_schedule()
all_tasks = scheduler.get_all_tasks()

if pet_filter != "All pets":
    schedule = scheduler.filter_by_pet(schedule, pet_filter)
    all_tasks = scheduler.filter_by_pet(all_tasks, pet_filter)

if status_filter == "Pending only":
    schedule = scheduler.filter_by_status(schedule, completed=False)
elif status_filter == "Completed only":
    schedule = scheduler.filter_by_status(all_tasks, completed=True)
    schedule = scheduler.sort_by_time(schedule)
else:
    schedule = scheduler.sort_by_time(
        scheduler.filter_by_status(all_tasks, completed=False)
        + scheduler.filter_by_status(all_tasks, completed=True)
    )

conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)

if schedule:
    rows = []
    for pet_name, task in schedule:
        rows.append(
            {
                "Time": task.time,
                "Task": task.description,
                "Pet": pet_name,
                "Frequency": task.frequency,
                "Status": "Completed" if task.completed else "Pending",
            }
        )
    st.table(rows)
else:
    st.info("No tasks scheduled yet. Add pets and tasks above.")

st.divider()

st.subheader("Complete a Task")
if owner.pets:
    complete_pet = st.selectbox(
        "Select pet to complete a task",
        [pet.name for pet in owner.pets],
        key="complete_pet",
    )
    pet_obj = owner.get_pet(complete_pet)
    if pet_obj and pet_obj.tasks:
        pending = [
            (i, t) for i, t in enumerate(pet_obj.tasks) if not t.completed
        ]
        if pending:
            task_labels = [
                f"{t.time} — {t.description} [{t.frequency}]" for _, t in pending
            ]
            selected_label = st.selectbox("Pending task", task_labels)
            selected_idx = task_labels.index(selected_label)
            actual_idx = pending[selected_idx][0]
            if st.button("Mark Complete"):
                scheduler.complete_task(complete_pet, actual_idx)
                st.success("Task marked complete!")
                if pet_obj.tasks[actual_idx].frequency in ("daily", "weekly"):
                    st.info("A new recurring instance was created for the next occurrence.")
                st.rerun()
        else:
            st.info(f"No pending tasks for {complete_pet}.")
    else:
        st.info(f"No tasks for {complete_pet} yet.")

st.divider()
st.caption(f"Managing {len(owner.pets)} pet(s) for {owner.name}.")
