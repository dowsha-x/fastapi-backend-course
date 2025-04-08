import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# Json для хранения задач
TASKS_FILE = "tasks.json"


# Модель задачи, которая будет использоваться для валидации данных
class Task(BaseModel):
    title: str
    status: str


def read_tasks_from_file():
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks


def write_tasks_to_file(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


@app.get("/tasks")
def get_tasks():
    tasks = read_tasks_from_file()
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    tasks = read_tasks_from_file()
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "status": task.status
    }
    tasks.append(new_task)
    write_tasks_to_file(tasks)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    tasks = read_tasks_from_file()
    for x in tasks:
        if x["id"] == task_id:
            x["title"] = task.title
            x["status"] = task.status
            write_tasks_to_file(tasks)
            return x
    raise HTTPException(status_code=404, detail="Таска не найдена!")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = read_tasks_from_file()
    task_to_delete = None
    for x in tasks:
        if x["id"] == task_id:
            task_to_delete = x
            break

    if task_to_delete:
        tasks.remove(task_to_delete)
        write_tasks_to_file(tasks)
        return {"сообщение": "Таска удалена!"}

    raise HTTPException(status_code=404, detail="Таска не найдена!")
