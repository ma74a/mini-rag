from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/")
def welcome(app_setting: Settings=Depends(get_settings)):
    app_name = app_setting.APP_NAME
    app_version = app_setting.APP_VERSION
    return {
        "app_name": app_name,
        "app_version": app_version
    }