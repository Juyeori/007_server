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
import pandas as pd
from sqlalchemy import *
from io import BytesIO

from db import engineconn
from models import Room

# fast api 초기화
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

# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#

@app.post("/api/image/upload")
async def create_upload_file(item: dict = Body(...)):
    engine = engineconn()
    session = engine.sessionmaker()

    # 여기 해야함
    teamname = item.get("teamname")
    username = item.get("username")
    
    # 이미지 저장
    try:
        sql = text("insert into image (teamname, username, image) values ('%s', '%s', '%s')" %(teamname, username, item.get("image")))
        result = session.execute(sql)
        session.commit()

    except:
        return {"msg" : "error"}
    

    # 이미지 합치기
    try:
        sql = text("select * from image where teamname = '%s'" %(teamname))
        result = session.execute(sql).fetchall()

        list = []
        for user in result:
            list.append(user[2])
            
        image = get_image(list)
        return {"image" : image}   
    except:
        return {"msg" : "error"}


#이미지 변환
def changeToImage(img):
    img = Image.open(io.BytesIO(base64.b64decode(img)))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    imgResize = cv2.resize(img, (300, 500))

    return imgResize

def get_image(list):
    image = changeToImage(list[0])

    for i in range(1, len(list)):
        image = cv2.addWeighted(image, 0.5, changeToImage(list[i]), 0.5, 5, 0)

    # cv2.imshow("img", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    result_image_pil = Image.fromarray(image)
    
    # Save the image to a BytesIO object
    buffer = BytesIO()
    result_image_pil.save(buffer, format="PNG")

    # 
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#
# -------------------------------------------------------------------------#


@app.post("/api/room")
async def get_room(item: dict = Body(...)):
    engine = engineconn()
    session = engine.sessionmaker()

    try:
        sql = text("select * from room where teamname = '%s'" %(item.get("teamname")))
        result = session.execute(sql).fetchall()

        if (len(result) != 0):
            return {"msg" : "success"}
        else:
            return {"msg" : "NoRoom"}    
    except:
        return {"msg" : "error"}
    

@app.post("/api/room/make")
async def create_room(item: dict = Body(...)):
    engine = engineconn()
    session = engine.sessionmaker()

    teamname = item.get("teamname")
    
    try:
        sql = text("insert into room (teamname) values ('%s')" %(teamname))
        result = session.execute(sql)
        session.commit()
        return {"msg" : "success"}
    except:
        return {"msg" : "error"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
