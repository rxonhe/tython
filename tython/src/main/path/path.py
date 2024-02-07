import os
from functools import cached_property
from typing import Optional

from tython import ROOT_DIR


class Path(str):

    def __init__(self, path: str):
        """
        :param path: Relative path from content root
        """
        self.path = path

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

    def read_py(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(self._get_module_name_from_path, self.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @cached_property
    def _get_module_name_from_path(self):
        base_name = os.path.basename(self.path)
        return os.path.splitext(base_name)[0]

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

    def prefix(self, prefix):
        return Path(os.path.join(prefix, str(self.path)))

    @property
    def exists(self):
        return os.path.exists(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path


class InternalPath(Path):

    def __init__(self, path: str):
        """
        :param path: Relative path from content root
        """
        super().__init__(path)
        self.path = os.path.join(ROOT_DIR, path.removeprefix("/"))
