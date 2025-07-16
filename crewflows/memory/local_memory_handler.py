import os
import json
from crewflows.memory.base import BaseMemoryHandler 

class LocalMemoryHandler(BaseMemoryHandler):
    def __init__(self, session_id: str, file_path: str):
        self.session_id = session_id
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def clear(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)