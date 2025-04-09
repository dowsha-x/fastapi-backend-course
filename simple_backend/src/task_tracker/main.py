import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("API_KEY")

app = FastAPI()

url = 'https://api.jsonbin.io/v3/b/'

headers = {
    "X-Master-Key": api_key
}

headers_type = {
  'Content-Type': 'application/json',
  'X-Master-Key': api_key
}


class Task(BaseModel):
    title: str
    status: str


# id таски для примера 67f554708960c979a580c3fb
# id таски для примера 67f554518561e97a50fb31fd
@app.get("/tasks/{task_id}")
def get_tasks(task_id: str):
    response = requests.get(f'{url}{task_id}', json=None, headers=headers)

    if response.status_code == 200:
        return response.json()
    raise HTTPException(
        status_code=response.status_code, detail="Не удалось получить задачи!"
    )


@app.post("/tasks")
def create_task(task: Task):
    data = {
        "title": task.title,
        "status": task.status
    }
    response = requests.post(url, json=data, headers=headers_type)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Не удалось создать задачу. Причина: {response.text}"
        )


@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    data = {
        "title": task.title,
        "status": task.status
    }
    response = requests.put(f'{url}{task_id}', json=data, headers=headers_type)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Не удалось изменить задачу. Причина: {response.text}"
        )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    response = requests.delete(f'{url}{task_id}', json=None, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Не удалось удалить задачу. Причина: {response.text}"
        )
