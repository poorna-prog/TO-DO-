import sqlite3
from datetime import datetime, timedelta

def detect_conflicts(new_due_time, conn, buffer_minutes=10):
    """Detect if the new task overlaps with any existing ones within a buffer."""
    cursor = conn.cursor()
    cursor.execute("SELECT title, due_time FROM tasks WHERE status = 'Pending'")
    tasks = cursor.fetchall()

    try:
        new_time = datetime.strptime(new_due_time, "%H:%M")
    except ValueError:
        return []

    conflicts = []
    for title, due in tasks:
        try:
            existing_time = datetime.strptime(due, "%H:%M")
        except ValueError:
            continue
        diff = abs((new_time - existing_time).total_seconds()) / 60
        if diff < buffer_minutes:
            conflicts.append((title, due))
    return conflicts
