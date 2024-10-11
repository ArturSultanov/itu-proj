import os

def get_file_path(user_id: str) -> str:
    return os.path.join("data", f"{user_id}.json")
