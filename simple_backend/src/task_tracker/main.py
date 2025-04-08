from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from task_file import TaskFile


app = FastAPI()


class Task(BaseModel):
    title: str
    status: str


@app.get("/tasks")
def get_tasks():
    tasks = TaskFile.read_tasks_from_file()
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    tasks = TaskFile.read_tasks_from_file()
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "status": task.status
    }
    tasks.append(new_task)
    TaskFile.write_tasks_to_file(tasks)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    tasks = TaskFile.read_tasks_from_file()
    for x in tasks:
        if x["id"] == task_id:
            x["title"] = task.title
            x["status"] = task.status
            TaskFile.write_tasks_to_file(tasks)
            return x
    raise HTTPException(status_code=404, detail="Таска не найдена!")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = TaskFile.read_tasks_from_file()
    task_to_delete = None
    for x in tasks:
        if x["id"] == task_id:
            task_to_delete = x
            break

    if task_to_delete:
        tasks.remove(task_to_delete)
        TaskFile.write_tasks_to_file(tasks)
        return {"сообщение": "Таска удалена!"}

    raise HTTPException(status_code=404, detail="Таска не найдена!")
