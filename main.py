from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import utils
import uvicorn
import os

from utils import generate_combined_outfit_text
# Initialize FastAPI
app = FastAPI()
origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)
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

# @app.post("/generate_image")
# async def generate_image(input):
#     image_url = utils.generate_image(input)
#     return {"ImageUrl": image_url}
#
# @app.post("/detect_image_web")
# async def detect_image_web(input):
#     imageResult = utils.detect_image_web(input)
#     return {"ImageResult:": imageResult}

@app.post("/flipkart_search")
async def flipkart_search(input):
    searchJson = utils.getFlipkartSearch(input)
    return {"SearchResult:": searchJson}



if __name__ == "__main__":
    uvicorn.run(app,port=int(os.environ.get('PORT', 8080)), host="0.0.0.0")
