import os
from typing import Optional

from dynamic_response_package.definitions import ROOT_DIR


class Path(str):

    def __init__(self, path):
        """
        :param path: Relative path from content root
        """
        self.path = os.path.join(ROOT_DIR, path.removeprefix("/"))

    def write_text(self, text):
        with open(self.path, "w") as f:
            f.write(text)
            f.close()

    def read_text(self) -> Optional[str]:
        try:
            with open(self.path, "r") as f:
                text = f.read()
                f.close()
        except FileNotFoundError:
            text = None
        return text

    def read_lines(self) -> Optional[list[str]]:
        try:
            with open(self.path, "r") as f:
                lines = f.readlines()
                f.close()
        except FileNotFoundError:
            lines = None
        return lines

    def read_json(self) -> Optional[dict]:
        import json
        try:
            with open(self.path, "r") as f:
                json_obj = json.load(f)
                f.close()
        except FileNotFoundError:
            json_obj = None
        return json_obj

    def write_json(self, json_obj):
        import json
        with open(self.path, "w") as f:
            json.dump(json_obj, f, indent=4)
            f.close()

    def join(self, *paths):
        paths_without_prefix = [path.removeprefix("/") for path in paths]
        return Path(os.path.join(str(self.path), *paths_without_prefix))

    def delete(self):
        os.remove(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path
