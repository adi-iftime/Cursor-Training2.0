from collections.abc import Generator
from contextlib import asynccontextmanager
from typing import Annotated

import sqlite3
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status

from task_tracker import crud, db
from task_tracker.schemas import TaskCreate, TaskOut, TaskPatch


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = db.get_connection()
    try:
        yield conn
    finally:
        conn.close()


DbConn = Annotated[sqlite3.Connection, Depends(get_db)]


@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, conn: DbConn) -> TaskOut:
    return crud.create_task(conn, payload.title)


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(conn: DbConn) -> list[TaskOut]:
    return crud.list_tasks(conn)


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, conn: DbConn) -> TaskOut:
    task = crud.get_task(conn, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def patch_task(task_id: int, payload: TaskPatch, conn: DbConn) -> TaskOut:
    task = crud.get_task(conn, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if payload.done is not None:
        crud.update_task_done(conn, task_id, payload.done)
    updated = crud.get_task(conn, task_id)
    assert updated is not None
    return updated


if __name__ == "__main__":
    uvicorn.run("task_tracker.main:app", host="127.0.0.1", port=8000, reload=True)
