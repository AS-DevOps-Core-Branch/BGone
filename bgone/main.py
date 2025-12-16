from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from withoutbg import remove
import shutil
import uuid

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_path = f"/tmp/{uuid.uuid4()}.jpg"
    output_path = f"/tmp/{uuid.uuid4()}.png"

    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
uvicorn main:app --host 0.0.0.0 --port 8000
uvicorn main:app --host 0.0.0.0 --port 8000

    # Remove background
    remove(input_path, output_path)

    return FileResponse(output_path, media_type="image/png")
