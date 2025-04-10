import os

def get_current_version():
    return os.getenv("APP_VERSION", "default")
