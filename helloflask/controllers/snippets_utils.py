import os
import sys
import json
from typing import Dict
from pathlib import Path


def get_constants() -> Dict[str, dict]:
    """"Parses ../constants.json file

    Return:
        dict: constants from constants.json
    """
    root_dir = Path(os.path.dirname(__file__)).parent
    constants_path = os.path.join(root_dir, 'constants.json')

    with open(constants_path) as constant_file:
        constants = json.load(constant_file)

    return constants


def read_snippets() -> Dict[str, str]:
    """Gets code snippets from ../snippets/snippets.py

    Returns:
        dict: Dictionary where each filename is a key and file 
                contents is the value to this key
    """

    root_dir = Path(os.path.dirname(__file__)).parent
    snippets_dir = os.path.join(root_dir, 'snippets')
    files = os.listdir(snippets_dir)
    snippets = {}
    for file in files:
        file_path = os.path.join(snippets_dir, file)
        if not os.path.isfile(file_path):
            continue
        with open(file_path) as snippet:
            snippets[file] = snippet.read()
    return snippets


def copy_snippets(project_name: str):
    """Creates new project files and copies snippets to the created files

    Args:
        project_name (str): current project name
    """

    from helloflask.controllers.venv_utils import set_flaskenv
    set_flaskenv()
    snippets = read_snippets()
    try:
        os.mkdir(project_name)
    except OSError as e:
        pass
        sys.exit(e)

    for file, content in snippets.items():
        if file == '__init__.py':
            continue
        if file.startswith('app'):
            path = os.path.join(project_name, file)
            with open(path, 'w') as snippet:
                snippet.write(content)
        else:
            with open(file, 'w') as snippet:
                imports = f'from {project_name}.app import app'
                content = f'{imports}\n{content}'
                snippet.write(content)
