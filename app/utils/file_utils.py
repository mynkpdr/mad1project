from app.config import BaseConfig
import time
import uuid
class FileUtils:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in BaseConfig.ALLOWED_EXTENSIONS
    
    @staticmethod
    def allowed_file_image(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in BaseConfig.ALLOWED_EXTENSIONS_IMAGE

    @staticmethod
    def get_unique_filename(filename):
        ext = filename.rsplit('.', 1)[1].lower()
        unique_name = str(int(time.time())) + "_" + str(uuid.uuid4()) + "." + ext
        return unique_name
    
    @staticmethod
    def is_file_size_allowed(file):
        file.seek(0, 2)  # Move the cursor to the end of the file
        file_size = file.tell()
        file.seek(0)  # Reset the cursor to the beginning of the file
        return file_size <= BaseConfig.MAX_FILE_SIZE