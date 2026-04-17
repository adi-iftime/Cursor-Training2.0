import sqlite3
from datetime import datetime, timezone

from task_tracker.schemas import TaskOut


def _row_to_task(row: sqlite3.Row) -> TaskOut:
    return TaskOut(
        id=row["id"],
        title=row["title"],
        done=bool(row["done"]),
        created_at=row["created_at"],
    )


def create_task(conn: sqlite3.Connection, title: str) -> TaskOut:
    created_at = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        "INSERT INTO tasks (title, done, created_at) VALUES (?, 0, ?)",
        (title, created_at),
    )
    conn.commit()
    task_id = int(cur.lastrowid)
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    assert row is not None
    return _row_to_task(row)


def list_tasks(conn: sqlite3.Connection) -> list[TaskOut]:
    rows = conn.execute("SELECT * FROM tasks ORDER BY id ASC").fetchall()
    return [_row_to_task(r) for r in rows]


def get_task(conn: sqlite3.Connection, task_id: int) -> TaskOut | None:
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return None
    return _row_to_task(row)


def update_task_done(conn: sqlite3.Connection, task_id: int, done: bool) -> bool:
    cur = conn.execute(
        "UPDATE tasks SET done = ? WHERE id = ?",
        (1 if done else 0, task_id),
    )
    conn.commit()
    return cur.rowcount > 0
