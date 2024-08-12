from fastapi import FastAPI, HTTPException # we import FastAPI for create application and it used create routing with 
#api httpexception used for error identify or find the error details and http status code is helpful to find errordetailed message like 500 internal server error
from motor.motor_asyncio import AsyncIOMotorClient #motor.motor_asyncio we import for interacte with mongodb asynchronous manner motor mongodb asynchronous motor
#asyncIOmotorclient it asynchronous client for mongodb it is interacte with fastapi asynchronus nature allowed non blocking database   
from bson import ObjectId # bson is module objectid class we import unique identifier dodcument object id is default unique identifier its automatically create id of documents
from typing import List# we import list from typing module because value provide list of values
from pydantic import BaseModel# basemodel class import from pydantic module itis used to create models (create studentmodel inside the model have studentdata)
import logging# itis used to debaugging and monitoring, error reporting, configuration and flexibility itis commonly used for recording events
 

app = FastAPI() #app is application fastapi is class this is create application 

# Configure logging
logging.basicConfig(level=logging.INFO) 

# MongoDB connection settings
MONGO_DETAILS = "mongodb://localhost:27017"# this used to connect mongodb localserver
client = AsyncIOMotorClient(MONGO_DETAILS) # we create client variable assign AsyncIOMotorClientclass(mongodetails)
database = client.students # create databse variable and assign client.students into database variable
student_collection = database.get_collection("students_collection") # itis  mongodb localserver database name and database collection this commend automatically genarate database and collection in mongodb localserver 

# Pydantic model for Student
class StudentModel(BaseModel):# studentmodel class created and inheriteby basemodel class
    name: str # name variable created and specifiy by variable string
    regno: str # regno variable created and specifiy by variable string
    father_name: str  # fathername variable created and specifiy by variable string

# Helper function to convert MongoDB document to dictionary
def student_helper(student) -> dict:# this commend purpose is create funtion and take the agument students 
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "regno": student["regno"],
        "father_name": student["father_name"]
    } # this returns values of student data

@app.get("/", tags=['root'])# it is used check correctly work your server basicly it is used check the api application
async def root() -> dict:
    return {"Ping": "Pong"} # it work return the msg inside in the return cmd

@app.get("/students", tags=['Students']) # this command contain get method and router and argument
async def get_students() -> List[dict]: # fastapi aysnu framework and create funtion our output return by dict inside list
    try: # error handling method
        students = [] # we create empty list for storing the value
        async for student in student_collection.find(): # we are assign student db in dbcollection find is motor curser
            print(type(student))# this commend check type of students
            students.append(student_helper(student))# this command is assign empty list with get function and inside student
        print(students) # print the students
        return students # return the students
    except Exception as e: # this command used to provide error detalis
        logging.error(f"Error fetching students: {e}") # this command used give identifying the issue
        raise HTTPException(status_code=500, detail="Internal Server Error") # this command is provide http status code with error details 

@app.post("/students", tags=["Students"]) # post method and students router 
async def add_student(student: StudentModel) -> dict:# fastapi aysnu framework and create funtion our output return by dict 
    try:
        new_student = await student_collection.insert_one(student.dict())
        created_student = await student_collection.find_one({"_id": new_student.inserted_id})
        return {
            "data": student_helper(created_student)
        } # this whole try is job in store post method it mean create new value
    except Exception as e:
        logging.error(f"Error adding student: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") # exception do provide error details and identifying error

@app.put("/students/{id}", tags=["Students"]) # update the storing value id mean default identifier 
async def update_student(id: str, body: StudentModel) -> dict:# this update the studentmodel
    try:
        updated_student = await student_collection.find_one_and_update(
            {"_id": ObjectId(id)},# the default id 
            {"$set": body.dict()},# the body it mean studentmodel 
            return_document=True
        )# this update the model
        if updated_student:
            return {
                "data": f"Student with id {id} has been updated"
            }# this return message for updated
        else:
            raise HTTPException(status_code=404, detail=f"Student with id {id} is not found!")# error msg nid not found based on status code
    except Exception as e:
        logging.error(f"Error updating student: {e}")# identify issue
        raise HTTPException(status_code=500, detail="Internal Server Error")# error msg base on status code

@app.delete("/students/{id}", tags=["Students"]) # this delete model
async def delete_student(id: str) -> dict: # give default id it delete whole model data
    try:
        deleted_student = await student_collection.find_one_and_delete({"_id": ObjectId(id)}) # this delete model data
        if deleted_student:
            return {
                "data": f"Student with id {id} has been deleted!"
            }# this deleted updated msg with id
        else:
            raise HTTPException(status_code=404, detail=f"Student with id {id} was not found!")# error msg nid not found based on status code
    except Exception as e:
        logging.error(f"Error deleting student: {e}")# identify issue
        raise HTTPException(status_code=500, detail="Internal Server Error")# error msg base on status code

