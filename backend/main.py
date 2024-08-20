from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

# MongoDB setup
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.bikes
bike_collection = database.get_collection("bikes_collection")

# CORS setup
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

class Bike(BaseModel):
    name: str
    color: str
    price: float

@app.post("/bikes/", response_model=Bike)
async def create_bike(bike: Bike):
    # Check if bike already exists
    if await bike_collection.find_one({"name": bike.name}):
        raise HTTPException(status_code=400, detail="Bike with this name already exists")
    
    # Insert new bike
    result = await bike_collection.insert_one(bike.dict())
    bike_id = result.inserted_id
    bike = await bike_collection.find_one({"_id": bike_id})
    return bike

@app.get("/bikes/", response_model=List[Bike])
async def get_bikes():
    bikes = await bike_collection.find().to_list(1000)
    return bikes

@app.get("/bikes/{bike_name}", response_model=Bike)
async def get_bike(bike_name: str):
    bike = await bike_collection.find_one({"name": bike_name})
    if bike:
        return bike
    raise HTTPException(status_code=404, detail="Bike not found")

@app.put("/bikes/{bike_name}", response_model=Bike)
async def update_bike(bike_name: str, updated_bike: Bike):
    result = await bike_collection.update_one(
        {"name": bike_name},
        {"$set": updated_bike.dict()}
    )
    if result.matched_count:
        bike = await bike_collection.find_one({"name": bike_name})
        return bike 
    raise HTTPException(status_code=404, detail="Bike not found")

@app.delete("/bikes/{bike_name}", response_model=Bike)
async def delete_bike(bike_name: str):
    bike = await bike_collection.find_one({"name": bike_name})
    if bike:
        await bike_collection.delete_one({"name": bike_name})
        return bike
    raise HTTPException(status_code=404, detail="Bike not found")
