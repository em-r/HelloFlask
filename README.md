# HelloFlask

Python library to automate boostrapping a Flask project.

## Features:

    - Sets up a virtual environment
    - Installs Flask and python-dotenv by default in the virtual environment
    - Installs third party libraries needed by the user asynchronously
    - Creates a flask app with boilerplate files

## Requirements:

    Python +3.6

## Installation:

    pip install helloflask

## Usage

    Run the command that suits you:
      - For Linux/Max users: helloflask project_name or python3 -m helloflask project_name
      - For windows users: python -m helloflask project_name

    You'll be then asked to type in the names of needed libraries:
    Example: `pytz flask-restful flask-sqlalchemy`

    After the packages are installed, instructions on how to use use the app will be displayed.
