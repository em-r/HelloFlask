import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="HelloFlask",
    version="1.2.0",
    description="Boostrap a Flask project with boilerplate and virtual environment.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ElMehdi19/HelloFlask",
    author="El Mehdi Rami",
    author_email="elmehdirami5@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6.*",
    install_requires=["colorama", "tqdm"],
    entry_points={
        "console_scripts": [
            "helloflask=helloflask.__main__:main",
        ]
    },
)
