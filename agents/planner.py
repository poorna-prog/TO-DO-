def add_task(title, description, due_time, conn):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, due_time) VALUES (?, ?, ?)",
        (title, description, due_time)
    )
    conn.commit()

def delete_task(task_id, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

def mark_done(task_id, conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
    conn.commit()
