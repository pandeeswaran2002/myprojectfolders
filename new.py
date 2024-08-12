from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List

app = FastAPI()

# MongoDB connection settings
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.todos
todo_collection = database.get_collection("todos_collection")


# Helper functions to convert MongoDB document to dictionary
def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "Activity": todo["Activity"]
    }


@app.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}


@app.get("/todo", tags=['Todos'], response_model=List[dict])
async def get_todos() -> List[dict]:
    todos = []
    async for todo in todo_collection.find():
        todos.append(todo_helper(todo))
    return {"Data": todos}


@app.post("/todo", tags=["Todos"])
async def add_todo(todo: dict) -> dict:
    new_todo = await todo_collection.insert_one(todo)
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return {
        "data": todo_helper(created_todo)
    }


@app.put("/todo/{id}", tags=["Todos"])
async def update_todo(id: str, body: dict) -> dict:
    updated_todo = await todo_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"Activity": body["Activity"]}},
        return_document=True
    )
    if updated_todo:
        return {
            "data": f"Todo with id {id} has been updated"
        }
    else:
        raise HTTPException(status_code=404, detail=f"This Todo with id {id} is not found!")


@app.delete("/todo/{id}", tags=["Todos"])
async def delete_todo(id: str) -> dict:
    deleted_todo = await todo_collection.find_one_and_delete({"_id": ObjectId(id)})
    if deleted_todo:
        return {
            "data": f"Todo with id {id} has been deleted!"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} was not found!")
