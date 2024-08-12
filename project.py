from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

MONGO_URL = "mongodb://localhost:27015"

client = AsyncIOMotorClient(MONGO_URL)
db = client.your_database_name  # Replace with your database name

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/todos")
async def get_todos():
    todos = await db.todos.find().to_list(1000)
    return {"message": "welcome everyone"}

@app.post("/todos")
async def create_todo(todo: dict):
    result = await db.todos.insert_one(todo)
    return {"id": str(result.inserted_id)}

