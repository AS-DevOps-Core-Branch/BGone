from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from rembg import remove
import uuid
import json
import os

app = FastAPI()

DB_FILE = "coins.json"

# Load or create coin DB
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def get_coins(user_id):
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    return data.get(user_id, 0)

def set_coins(user_id, coins):
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    data[user_id] = coins
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

@app.post("/register")
def register():
    user_id = str(uuid.uuid4())
    set_coins(user_id, 3)  # 🎁 free coins
    return {"user_id": user_id, "coins": 3}

@app.post("/add-coin")
def add_coin(user_id: str):
    coins = get_coins(user_id) + 1
    set_coins(user_id, coins)
    return {"coins": coins}

@app.post("/remove-bg")
async def remove_bg(user_id: str, file: UploadFile = File(...)):
    coins = get_coins(user_id)
    if coins <= 0:
        raise HTTPException(status_code=402, detail="No coins left")

    input_bytes = await file.read()
    output_bytes = remove(input_bytes)

    set_coins(user_id, coins - 1)

    output_path = f"/tmp/{uuid.uuid4()}.png"
    with open(output_path, "wb") as f:
        f.write(output_bytes)

    return FileResponse(output_path, media_type="image/png")

