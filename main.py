from fastapi import FastAPI, File, UploadFile
import pymongo
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

# Initialize MongoDB client and collection
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["items"]

class Item(BaseModel):
    name: str
    image: UploadFile  # Use UploadFile for image data
    like: int
    comments: str

@app.post("/items/")
async def create_item(item: Item):
    # Save the uploaded image to the filesystem (you may want to use a dedicated storage solution in production)
    with open(item.image.filename, "wb") as f:
        f.write(item.image.file.read())

    # Store information about the image in MongoDB
    item_data = {
        "username": item.name,
        "image_filename": item.image.filename,  # Save the image filename in the database
        "like": item.like,
        "comments": item.comments,
    }
    
    result = mycol.insert_one(item_data)

    return JSONResponse(content=jsonable_encoder({"message": "Item created successfully", "item_id": str(result.inserted_id)}))
