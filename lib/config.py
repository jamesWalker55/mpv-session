import json
import os.path

# __file__ returns the path of THIS file
# since this file is in lib/, you need to go up 2 levels
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    def __init__(self, path) -> None:
        self.path = path
        self.load()

    def get_config_path(self):
        return os.path.abspath(os.path.join(BASE_DIR, self.path))

    def load(self):
        try:
            with open(self.get_config_path(), "r", encoding="utf8") as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.data = None

    def save(self):
        with open(self.get_config_path(), "w", encoding="utf8") as f:
            if self.data is None:
                # create an empty file
                pass
            else:
                json.dump(self.data, f)
