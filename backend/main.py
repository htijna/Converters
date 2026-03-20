import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from services.converter import FileConverter
from services.utils import cleanup_old_files, safe_remove

UPLOAD_DIR = "uploads"
CONV_DIR = "converted"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(CONV_DIR, exist_ok=True)
    yield
    # Cleanup (Optional)

app = FastAPI(title="AKJ Converter API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    try:
        # Periodic cleanup of old files in the background
        background_tasks.add_task(cleanup_old_files, UPLOAD_DIR)
        background_tasks.add_task(cleanup_old_files, CONV_DIR)

        # 25MB check
        file_size = 0
        file_ext = file.filename.split(".")[-1].lower()
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_DIR, f"{file_id}.{file_ext}")
        output_filename = f"{file_id}.{target_format}"
        output_path = os.path.join(CONV_DIR, output_filename)

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(input_path)
        if file_size > 25 * 1024 * 1024:
            safe_remove(input_path)
            raise HTTPException(status_code=400, detail="File too large (max 25MB)")

        converter = FileConverter.get_converter(file_ext, target_format)
        if not converter:
            safe_remove(input_path)
            raise HTTPException(status_code=400, detail=f"Conversion from {file_ext} to {target_format} not supported.")

        # Run conversion
        converter(input_path, output_path)

        # Cleanup input file
        background_tasks.add_task(safe_remove, input_path)
        
        return {
            "status": "success",
            "download_url": f"/download/{output_filename}",
            "filename": f"converted_{file.filename.split('.')[0]}.{target_format}"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error: {e}")
        # Ensure input file is removed if error occurs
        if 'input_path' in locals(): safe_remove(input_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str, dname: str = None):
    file_path = os.path.join(CONV_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, 
            detail="Download link has expired. Please convert the file again."
        )
    
    return FileResponse(
        path=file_path, 
        filename=dname or filename,
        media_type='application/octet-stream'
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

