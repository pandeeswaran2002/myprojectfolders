from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define the To-Do item model
class TodoItem(BaseModel):
    id: int
    task: str
    completed: bool = True

# In-memory storage for to-do items
todo_list: List[TodoItem] = []

# Helper function to find a to-do item by ID
def find_todo_item(item_id: int) -> Optional[TodoItem]:
    return next((item for item in todo_list if item.id == item_id), None)

# PUT method to update an existing to-do item
@app.put("/todos/{item_id}", response_model=TodoItem)
def update_todo(item_id: int, updated_todo: TodoItem):
    todo_item = find_todo_item(item_id)
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found.")
    todo_item.task = updated_todo.task
    todo_item.completed = updated_todo.completed
    return todo_item

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
