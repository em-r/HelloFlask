import os
import re
import sys
from typing import List
from colorama import Fore
from helloflask.controllers.snippets_utils import get_constants


def unspecified_project_name():
    print(Fore.RED)
    print('Error: No project name was specified.')
    print('Please run the following command: python -m helloflask <project-name>')
    print('Example: python -m helloflask my-blog')
    print(Fore.RESET)


def invalid_project_name():
    print(Fore.RED)
    print('Error: Invalid project name')
    print('Hint: Project names can`t start with a number')
    print('Hint: Project names consist only of letters, numbers and underscores')
    print('Examples: my_app, my_app_1, myApp')
    print(Fore.RESET)


def verify_project_name(project_name: str) -> bool:
    """Checks project name against a regex pattern

    Args:
        project_name (str): current project name

    Returns:
        bool: true if there was a match
              False if there was no match
    """
    pattern = re.compile(r'^[a-z][a-z0-9_]{1,}$', re.I)
    matches = pattern.match(project_name)

    return matches


def wrap_string(string: str, color: str) -> str:
    """Wraps a given string between colorama color codes to change 
        the string's color

    Args:
        string (str): string to be colored
        color (str): color to be used to color the string

    Returns:
        str: string wrapped within the color codes from colorama
    """

    wrapper = getattr(Fore, color.upper())
    reset = Fore.RESET
    return f'{wrapper}{string}{reset}'


def creating_app_str(project_name: str) -> str:
    string_1 = wrap_string('Creating Flask project', 'yellow')
    string_2 = wrap_string(project_name, 'green')
    return f'{string_1} {string_2}\n'


def creating_venv_str() -> str:
    string = 'Setting up virtual environment... This won`t take too long'
    output = wrap_string(string, 'yellow')
    return output


def to_be_installed_str(packages: List[str], on=False) -> str:
    string = wrap_string(', '.join(packages), 'cyan')
    if on:
        output = f'Installing: {string}\n'
        return output

    return f'Packages to be installed: {string}\n'


def installed_packages_str(packages: int, dependencies: int, timing: float) -> str:
    string = f'Installed {packages} package(s) and {dependencies} dependencies in {timing} seconds'
    output = wrap_string(string, 'yellow')
    return f'{output}\n'


def list_packages_str(installed_packages: List[str]) -> str:
    packages = list(map(lambda x: wrap_string(
        f"\t+ {x.replace('==', '@')}", 'green'), installed_packages))
    string = '\n'.join(packages)
    return f'Installed Packages: \n{string}\n'


def success_exit(project_name: str, project_path: str):
    from helloflask.controllers.os_utils import get_os

    current_os = get_os()
    print(f'Success! Created {project_name} at {project_path}', end='\n\n')
    print('We suggest that you begin by typing: ', end='\n\n')

    base_name = wrap_string(os.path.basename(project_path), 'yellow')
    print(f'\t{Fore.CYAN}cd{Fore.RESET} {base_name}')

    os_constants = get_constants().get(current_os)
    activate_venv = wrap_string(os_constants.get('ACTIVATE_VENV'), 'yellow')
    print(f'\t{activate_venv}')

    flask_run = wrap_string('flask run', 'cyan')
    print(f'\t{flask_run}', end='\n\n')

    closing_message = wrap_string('Happy Flasking', 'green')
    print(closing_message)

    sys.exit(0)
