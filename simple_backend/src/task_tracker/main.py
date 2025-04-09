import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from constans import (url, headers, headers_type,
                      API_BASE_URL, LLM_MODEL, HEADERS_AI)


app = FastAPI()


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


def run_llm(model: str, task_text: str) -> str:
    inputs = [
        { "role": "system", "content": "Ты — дружелюбный помощник, который объясняет, как решать задачи." },
        { "role": "user", "content": f"Объясни, как решить задачу на русском языке: {task_text}" }
    ]
    input_payload = {"messages": inputs}
    response = requests.post(
        f"{API_BASE_URL}{model}",
        headers=HEADERS_AI,
        json=input_payload
    )
    if response.status_code == 200:
        return response.json()["result"]["response"]
    else:
        raise Exception(
            f"Ошибка LLM: {response.status_code} - {response.text}"
        )


@app.post("/tasks")
def create_task(task: Task):
    try:
        explanation = run_llm(LLM_MODEL, task.title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка LLM: {str(e)}")

    data = {
        "title": task.title,
        "status": task.status,
        "explanation": explanation
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
