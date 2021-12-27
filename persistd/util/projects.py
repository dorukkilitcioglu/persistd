import os
from typing import List

from persistd.util.settings import SETTINGS


def get_all_projects(base_path: str = SETTINGS.base_path, only_initialized: bool = False) -> List[str]:
    projects = [d for d in next(os.walk(base_path))[1] if not d.startswith('.')]
    if not only_initialized:
        return projects
    projects = [project_name for project_name in projects if
                os.path.exists(os.path.join(base_path, project_name, '.persistd', 'pd.json'))]
    return projects
