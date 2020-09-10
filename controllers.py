import os
import sys
import time
import json
import subprocess
import platform
from random import sample, shuffle
from string import ascii_lowercase, digits
from typing import List, Union, Dict


def get_os() -> Union[str]:
    os = platform.system().lower()
    if 'win' in os:
        return 'windows'

    elif any(['linux' in os, 'darwin' in os]):
        return 'linux'

    else:
        sys.exit('Error: system not supported yet')


def gen_folder_name(project_name: str) -> str:
    random_lower = sample(ascii_lowercase, 3)
    random_digits = sample(digits, 3)
    random_comb = [*random_lower, *random_digits]
    shuffle(random_comb)
    random_comb = ''.join(random_comb)
    return f'{project_name}_{random_comb}'


def read_snippets() -> Dict[str, str]:
    root_dir = os.path.dirname(__file__)
    snippets_dir = os.path.join(root_dir, 'snippets')
    files = os.listdir(snippets_dir)
    snippets = {}
    for file in files:
        file_path = os.path.join(snippets_dir, file)
        with open(file_path) as snippet:
            snippets[file] = snippet.read()
    return snippets


def get_constants() -> Dict[str, dict]:
    root_dir = os.path.dirname(__file__)
    constants_path = os.path.join(root_dir, 'constants.json')

    with open(constants_path) as constant_file:
        constants = json.load(constant_file)

    return constants


def venv_init():
    current_os = get_os()
    if current_os == 'linux':
        init_venv_process = subprocess.run(
            ['python3', '-m', 'venv', 'venv'], capture_output=True)
    else:
        init_venv_process = subprocess.run(
            "python -m venv venv", capture_output=False, shell=True)
    if init_venv_process.returncode:
        # stderr = init_venv_process.stderr.decode()
        sys.exit('error')


def get_env(project_path):
    env = os.environ.copy()
    current_os = get_os()

    paths = get_constants().get(current_os)

    python_path = paths.get('PYTHON3_PATH')
    pip_path = paths.get('PIP3_PATH')
    env['PATH'] = os.path.join(project_path, python_path)
    pip = os.path.join(project_path, pip_path)

    return [env, pip]


def get_packages() -> List[str]:
    defaults = ['flask', 'python-dotenv']
    print('Packages to be installed: flask, python-dotenv\n')
    extra_packages = input('Add packages (space separated): ').split()
    if not extra_packages:
        return defaults
    return [*defaults, *extra_packages]


def get_installed_packages(project_path) -> List[str]:
    env, pip = get_env(project_path)
    packages = subprocess.run([pip, 'freeze'], capture_output=True, env=env)
    installed_packages = packages.stdout.decode().strip().split('\n')
    total_packages = len(installed_packages)
    return [installed_packages, total_packages]


def set_flaskenv():
    try:
        with open('.flaskenv', 'w') as flaskenv:
            env_vars = ['FLASK_APP=run.py', 'FLASK_ENV=development']
            flaskenv.write('\n'.join(env_vars))

    except OSError as e:
        sys.exit(e)


def venv_install_packages(project_path: str):
    venv_init()

    env, pip = get_env(project_path)
    needed_packages = get_packages()

    print('Installing: ', ', '.join(needed_packages))
    start = time.perf_counter()
    subprocess.run([pip, 'install', *needed_packages],
                   capture_output=True, env=env)
    finish = time.perf_counter()
    timing = round(finish - start, 3)

    installed_packages, total_packages = get_installed_packages(project_path)
    total_main_packages = len(needed_packages)
    total_dependencies = total_packages - total_main_packages

    print(
        f'Installed {total_main_packages} package(s) {total_dependencies} dependencies in {timing} seconds')
    packages = list(map(lambda x: x.replace('==', '@'), installed_packages))
    print('Packages: ', *packages, sep='\n')


def copy_snippets(project_name: str):
    set_flaskenv()
    snippets = read_snippets()
    try:
        os.mkdir(project_name)
    except OSError as e:
        pass
        sys.exit(e)

    for file, content in snippets.items():
        if file.startswith('app'):
            path = os.path.join(project_name, file)
            with open(path, 'w') as snippet:
                snippet.write(content)
        else:
            with open(file, 'w') as snippet:
                imports = f'from {project_name}.app import app'
                content = f'{imports}\n{content}'
                snippet.write(content)
