import os
import sys
import subprocess
import time
from random import sample, shuffle
from string import ascii_lowercase, digits
from typing import List, Union, Dict


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


def venv_init():
    init_venv_process = subprocess.run(
        ['python3', '-m', 'venv', 'venv'], capture_output=True)

    if init_venv_process.returncode:
        stderr = init_venv_process.stderr.decode()
        sys.exit(stderr)


def get_env(project_path) -> List[Union[dict, str]]:
    env = os.environ.copy()
    env['PATH'] = os.path.join(project_path, 'venv/bin/python3')
    pip = os.path.join(project_path, 'venv/bin/pip3')
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
    subprocess.run([pip, 'install', *needed_packages], capture_output=True)
    finish = time.perf_counter()
    timing = round(finish - start, 3)

    installed_packages, total_packages = get_installed_packages(project_path)
    print(f'Installed {total_packages} package(s) in {timing} seconds')
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
