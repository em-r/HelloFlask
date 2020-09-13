import os
import sys
import subprocess
from controllers.os_utils import get_os
from controllers.snippets_utils import get_constants
from controllers.ui_utils import creating_venv_str


def venv_init():
    current_os = get_os()
    print(creating_venv_str())
    if current_os == 'linux':
        init_venv_process = subprocess.run(
            ['python3', '-m', 'venv', 'venv'], capture_output=True)
    else:
        init_venv_process = subprocess.run(
            "python -m venv venv", capture_output=False, shell=True)
    if init_venv_process.returncode:
        stderr = init_venv_process.stderr.decode()
        sys.exit(stderr)


def get_env_vars(project_path):
    env = os.environ.copy()
    current_os = get_os()

    paths = get_constants().get(current_os)

    python_path = paths.get('PYTHON3_PATH')
    pip_path = paths.get('PIP3_PATH')
    env['PATH'] = os.path.join(project_path, python_path)
    pip = os.path.join(project_path, pip_path)

    return [env, pip]


def set_flaskenv():
    try:
        with open('.flaskenv', 'w') as flaskenv:
            env_vars = ['FLASK_APP=run.py', 'FLASK_ENV=development']
            flaskenv.write('\n'.join(env_vars))

    except OSError as e:
        sys.exit(e)
