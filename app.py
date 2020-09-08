import os
import sys
import argparse
from classes import OpenDir
from controllers import gen_folder_name, venv_init, venv_install_packages, copy_snippets

parser = argparse.ArgumentParser()
parser.add_argument('project_name', type=str, help='Project name')
args = parser.parse_args()

root_dir = os.getcwd()

try:
    project_name = args.project_name
except AttributeError:
    sys.exit('please provide a project_name')

try:
    project_path = os.path.join(root_dir, project_name)
    os.mkdir(project_path)

except OSError:
    pass
    while True:
        new_dir_name = gen_folder_name(project_name)
        project_path = os.path.join(root_dir, new_dir_name)
        if not os.path.isdir(project_path):
            os.mkdir(project_path)
            break

with OpenDir(project_path):
    print(f'Creating flask project {project_name}')
    print(f'Setting up virtual environment...')
    venv_install_packages(project_path)
    copy_snippets(project_name)
