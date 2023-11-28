# main.py

from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
import cv2
from starlette.requests import Request
import base64
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home():
    return "hello world"


@app.post("/upload")
async def create_upload_file(item: dict = Body(...)):
    changeToImage(item.get("image"))
    return {"image": item}

#이미지 변환
def changeToImage(img):
    img = Image.open(io.BytesIO(base64.b64decode(img)))
    img = np.array(img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    imgResize = cv2.resize(img, (300, 500))
    # max_output_value = 255   # 출력 픽셀 강도의 최대값
    # neighborhood_size = 99
    # subtract_from_mean = 10
    # imageBinarized = cv2.adaptiveThreshold(imgResize,
    #                                     max_output_value,
    #                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                     cv2.THRESH_BINARY,
    #                                     neighborhood_size,
    #                                     subtract_from_mean)
    
    cv2.imshow("img", imgResize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
