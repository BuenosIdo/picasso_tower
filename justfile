#!/usr/bin/env just --justfile

python_executable := "python3.10"
venv_folder_name := "venv"
venv_executable := venv_folder_name + "/bin/python"


apt-installations:
  sudo apt-get install python3.10 python3.10-venv

create-venv:
  {{python_executable}} -m venv venv

install_project:
  {{venv_executable}} -m pip install -e .[dev]

setup: apt-installations create-venv install_project

format:
  isort --line-length 120 picasso test
  black --line-length 120 picasso test

lint:
  flake8 picasso test
  mypy picasso test

test:
  pytest