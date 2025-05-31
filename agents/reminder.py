import datetime

def check_due_tasks(conn):
    now = datetime.datetime.now().time()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE status='Pending'")
    tasks = cursor.fetchall()
    upcoming = []
    for task in tasks:
        task_time = datetime.datetime.strptime(task[3], "%H:%M").time()
        if task_time <= (datetime.datetime.now() + datetime.timedelta(minutes=10)).time():
            upcoming.append(task)
    return upcoming
