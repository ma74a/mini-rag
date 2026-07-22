from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
import aiofiles
import logging

from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, 
                       file: UploadFile,
                       app_setting: Settings=Depends(get_settings)):

    data_controller = DataController()
    # validate the file properites
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
                                                original_filename=file.filename, 
                                                project_id=project_id
                                            )

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_setting.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
         logger.error(f"Error while uploading file: {e}")
         return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "signal": ResponseSignal.FILE_UPLOADED_FAILED.value
                    }
                )


    return JSONResponse(
                content={
                    "signal": ResponseSignal.FILE_UPLOADED_SUCCESSED.value,
                    "file_id": file_id
                }
            )