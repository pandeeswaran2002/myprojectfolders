from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pydantic import BaseModel
from typing import List
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS) 
database = client.cars 
car_collection = database.get_collection("cars_collection") 

class carmodel(BaseModel):
    brand:str
    model:str
    price:str

def car_helper(car) -> dict:
    return {
        "id": str(car["_id"]),
        "brand": car["brand"],
        "model": car["model"],
        "price": car["price"]
    } 




@app.get("/cars", tags=['cars'])
async def get_cars() -> List[dict]: 
    try: 
        cars = [] 
        async for car in car_collection.find(): 
            print(type(car))
            cars.append(car_helper(car))
        print(cars)
        return cars 
        
    except Exception as e: 
        logging.error(f"Error fetching cars: {e}") 
        raise HTTPException(status_code=500, detail="Internal Server Error") 

@app.post("/cars", tags=["cars"]) 
async def add_car(car: carmodel) -> dict:
    try:
        new_car = await car_collection.insert_one(car.dict())
        created_car = await car_collection.find_one({"_id": new_car.inserted_id})
        return {
            "data": car_helper(created_car)
        } 
    except Exception as e:
        logging.error(f"Error adding car: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/cars/{id}", tags=["cars"])
async def update_car(id: str, body: carmodel) -> dict:
    try:
        updated_car = await car_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": body.dict()},
            return_document=True
        )
        if updated_car:
            return {
                "data": f"car with id {id} has been updated"
            }
        else:
            raise HTTPException(status_code=404, detail=f"car with id {id} is not found!")
    except Exception as e:
        logging.error(f"Error updating car: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/cars/{id}", tags=["cars"])
async def delete_car(id: str) -> dict: 
    try:
        deleted_car = await car_collection.find_one_and_delete({"_id": ObjectId(id)}) 
        if deleted_car:
            return {
                "data": f"car with id {id} has been deleted!"
            }
        else:
            raise HTTPException(status_code=404, detail=f"car with id {id} was not found!")
    except Exception as e:
        logging.error(f"Error deleting car: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")






    








