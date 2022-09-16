# Contribution Guidelines

## Setup

This project builds and installs with [Poetry](https://python-poetry.org/) and
[PyInstaller](https://pyinstaller.org/en/stable/).

After downloading the repository and installing poetry, you can install dependencies and pre-commit checks with

`poetry install`  
`poetry run pre-commit install`

An executable for your operating system may be built with:  
`poetry run pyinstaller __main__.spec`
