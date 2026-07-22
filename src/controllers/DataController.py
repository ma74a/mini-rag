from fastapi import UploadFile
import os
import re

from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024*1024

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_setting.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        # size with bytes, but file_max_size with megabytes
        if file.size > self.app_setting.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATE_SUCCUESS.value

    def generate_unique_filepath(self, original_filename: str, project_id: str):
        random_key = self.generate_random_string()
        project_dir_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.get_clean_file_name(orig_file_name=original_filename)

        new_file_path = os.path.join(project_dir_path, random_key + "_" + cleaned_filename)

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_dir_path,
                random_key + "_" + cleaned_filename
            )

        return new_file_path, random_key + "_" + cleaned_filename

    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name