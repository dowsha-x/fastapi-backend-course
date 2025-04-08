from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# Список для хранения задач
tasks = []


# Модель задачи, которая будет использоваться для валидации данных
class Task(BaseModel):
    title: str
    status: str


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "status": task.status
    }
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for x in tasks:
        if x["id"] == task_id:
            x["title"] = task.title
            x["status"] = task.status
            return x
    raise HTTPException(status_code=404, detail="Таска не найдена!")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    task_to_delete = None
    for x in tasks:
        if x["id"] == task_id:
            task_to_delete = x
            break

    if task_to_delete:
        tasks.remove(task_to_delete)
        return {"сообщение": "Таска удалена!"}

    raise HTTPException(status_code=404, detail="Таска не найдена!")
