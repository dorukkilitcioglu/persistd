from __future__ import annotations

import dataclasses
import os
from typing import Optional, List

from dataclasses_json import dataclass_json

from persistd.util.paths import SETTINGS_PATH

LOCAL_SETTINGS_PATH = os.path.join(SETTINGS_PATH, 'local.json')


@dataclass_json
@dataclasses.dataclass
class Settings:
    base_path: str = "C:\\Users\\doruk\\Desktop\\Playground"
    file_path: str = LOCAL_SETTINGS_PATH

    # Program Paths
    sublime_text_path: str = "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
    conemu_path: str = "C:\\Tools\\ConEmu\\ConEmu64.exe"
    chrome_path: str = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    vscode_path: str = "C:\\Users\\doruk\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"

    # Projects
    open_projects: List[str] = dataclasses.field(default_factory=list)

    @classmethod
    def field_names(cls):
        return [field for field in cls.__dataclass_fields__]

    @staticmethod
    def load(json_file: str = LOCAL_SETTINGS_PATH, missing_ok: bool = False) -> Settings:
        if not os.path.exists(json_file):
            if missing_ok:
                return Settings(file_path=json_file)
            raise ValueError(f"There is no settings file at {json_file}")
        with open(json_file, 'r') as fp:
            content = fp.read()
            if not content:
                if missing_ok:
                    return Settings(file_path=json_file)
                raise ValueError(f"The settings file is empty at {json_file}")
            return Settings.from_json(content)

    def save(self, json_file: Optional[str] = None) -> Settings:
        file_path = json_file if json_file else self.file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as fp:
            fp.write(self.to_json(indent=4))
        return self

    def add_open_project(self, project: str, save: bool = True) -> Settings:
        if project in self.open_projects:
            raise ValueError("This project is already open!")
        self.open_projects.append(project)
        if save:
            self.save()
        return self

    def remove_open_project(self, project: str, save: bool = True) -> Settings:
        if project not in self.open_projects:
            raise ValueError("This project is not open!")
        self.open_projects.remove(project)
        if save:
            self.save()
        return self


# Initialize the settings singleton
SETTINGS = Settings.load(missing_ok=True).save()
