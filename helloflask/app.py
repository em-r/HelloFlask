import os
import sys
import argparse
import colorama

from classes import OpenDir
from controllers.os_utils import gen_folder_name
from controllers.venv_utils import venv_init
from controllers.packages_utils import install_packages
from controllers.snippets_utils import copy_snippets
from controllers.ui_utils import (verify_project_name,
                                  unspecified_project_name,
                                  invalid_project_name,
                                  creating_app_str,
                                  success_exit
                                  )


def read_from_user():
    parser = argparse.ArgumentParser()
    parser.add_argument('project_name', type=str, help='Project name')
    args = parser.parse_args()

    try:
        project_name = args.project_name

    except AttributeError:
        unspecified_project_name()
        sys.exit(1)

    if not verify_project_name(project_name):
        invalid_project_name()
        sys.exit(1)

    return project_name


def main():
    colorama.init()

    project_name = read_from_user()
    root_dir = os.getcwd()

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
        print(creating_app_str(project_name))
        install_packages(project_path)
        copy_snippets(project_name)
        success_exit(project_name, project_path)
