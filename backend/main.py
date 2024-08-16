from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://127.0.0.1:8002",  # Frontend server URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory storage for bike details
bikes = []

class Bike(BaseModel):
    name: str
    color: str
    price: float

@app.post("/bikes/", response_model=Bike)
def create_bike(bike: Bike):
    bikes.append(bike)
    return bike

@app.get("/bikes/", response_model=List[Bike])
def get_bikes():
    return bikes

@app.get("/bikes/{bike_name}", response_model=Bike)
def get_bike(bike_name: str):
    for bike in bikes:
        if bike.name == bike_name:
            return bike
    raise HTTPException(status_code=404, detail="Bike not found")

@app.delete("/bikes/{bike_name}", response_model=Bike)
def delete_bike(bike_name: str):
    global bikes
    for bike in bikes:
        if bike.name == bike_name:
            bikes = [b for b in bikes if b.name != bike_name]
            return bike
    raise HTTPException(status_code=404, detail="Bike not found")
