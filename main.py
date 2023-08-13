from fastapi import FastAPI

import utils
import uvicorn
import os

from utils import generate_combined_outfit_text
# Initialize FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}

@app.post("/combined_outfit_text")
async def generate_combined_outfit_text(input):
    combinedOutfit = utils.generate_combined_outfit_text(input)
    return {"Output": combinedOutfit}

@app.post("/generate_image")
async def generate_image(input):
    image_url = utils.generate_image(input)
    return {"ImageUrl": image_url}

@app.post("/detect_image_web")
async def detect_image_web(input):
    imageResult = utils.detect_image_web(input)
    return {"ImageResult:": imageResult}


if __name__ == "__main__":
    uvicorn.run(app,port=int(os.environ.get('PORT', 8080)), host="0.0.0.0")
