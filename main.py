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

@app.get("/combined_outfit_text")
async def generate_combined_outfit_text(input):
    combinedOutfit = utils.generate_combined_outfit_text(input)
    #print(combinedOutfit)
    return combinedOutfit


@app.get("/flipkart_search")
async def flipkart_search(input):
    searchJson = utils.getMultipleFlipkartSearch(input)
    return searchJson



if __name__ == "__main__":
    uvicorn.run(app,port=int(os.environ.get('PORT', 8080)), host="0.0.0.0")
