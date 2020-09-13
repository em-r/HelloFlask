import subprocess
import time
from typing import List
from helloflask.controllers.venv_utils import venv_init, get_env_vars
from helloflask.controllers.ui_utils import (installed_packages_str,
                                             to_be_installed_str,
                                             list_packages_str)


def get_user_packages() -> List[str]:
    """Reads packages names from user input

    Returns:
        list: List containing the defaults packages and packages supplied by the user
    """

    defaults = ['flask', 'python-dotenv']
    print(to_be_installed_str(defaults))
    extra_packages = input('Add packages (space separated): ').split()
    if not extra_packages:
        return defaults
    return [*defaults, *extra_packages]


def install_packages(project_path: str):
    """Installs packages in virtual environment

    Args:
        project_path (str): Path to where the project lives
    """

    venv_init()

    env, pip = get_env_vars(project_path)
    needed_packages = get_user_packages()

    print(to_be_installed_str(needed_packages, on=True))

    start = time.perf_counter()
    subprocess.run([pip, 'install', *needed_packages],
                   capture_output=True, env=env)
    finish = time.perf_counter()
    timing = round(finish - start, 3)

    installed_packages, total_packages = get_installed_packages(project_path)
    total_main_packages = len(needed_packages)
    total_dependencies = total_packages - total_main_packages

    print(installed_packages_str(total_main_packages, total_dependencies, timing))
    print(list_packages_str(installed_packages))


def get_installed_packages(project_path: str) -> List[str]:
    """Gets list of installed packages in the virtual environment

    Args:
        project_path (str): Path to where the project lives

    Returns:
        list: List of installed packages
    """

    env, pip = get_env_vars(project_path)
    packages = subprocess.run([pip, 'freeze'], capture_output=True, env=env)
    installed_packages = packages.stdout.decode().strip().split('\n')
    total_packages = len(installed_packages)
    return [installed_packages, total_packages]
