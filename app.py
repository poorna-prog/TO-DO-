import streamlit as st
from agents import planner, scheduler, reminder
from utils.db_handler import get_connection, get_all_tasks

import datetime

# Must be first Streamlit call
st.set_page_config(page_title="Multi-Agent To-Do App", layout="wide")

# Inject custom CSS
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #f8f9fa, #e0c3fc);
    font-family: 'Segoe UI', sans-serif;
}
h1 {
    color: #6a11cb;
}
.stButton>button {
    background-color: #6a11cb;
    color: white;
    border-radius: 12px;
    padding: 0.5em 1em;
}
.stButton>button:hover {
    background-color: #2575fc;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Smart Multi-Agent To-Do & Reminder App")

conn = get_connection()

with st.form("task_form"):
    title = st.text_input("Task Title")
    description = st.text_area("Description")
    due_time = st.time_input("Due Time", value=datetime.datetime.now().time())
    submitted = st.form_submit_button("Add Task")

    if submitted:
        time_str = due_time.strftime("%H:%M")
        conflicts = scheduler.detect_conflicts(time_str, conn)
        if conflicts:
            st.error(f"⚠️ Conflict with: {', '.join([c[0] for c in conflicts])}")
        else:
            planner.add_task(title, description, time_str, conn)
            st.success("✅ Task added successfully!")

# Display tasks
st.markdown("### 📝 Your Tasks")
tasks = get_all_tasks()
for task in tasks:
    col1, col2, col3 = st.columns([4, 2, 2])
    col1.write(f"**{task[1]}** - {task[2]}")
    col2.write(f"Due: {task[3]}")
    with col3:
        if st.button("✅ Done", key=f"done{task[0]}"):
            planner.mark_done(task[0], conn)
        if st.button("❌ Delete", key=f"del{task[0]}"):
            planner.delete_task(task[0], conn)

# Alert Section
st.markdown("### 🔔 Alerts")
alerts = reminder.check_due_tasks(conn)
for alert in alerts:
    st.warning(f"⏰ Task '{alert[1]}' is due soon at {alert[3]}!")
