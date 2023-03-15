#!/usr/bin/env just --justfile

python_executable := "python3.10"
venv_folder_name := "venv"
venv_executable := venv_folder_name + "/bin/python"


apt-installations:
  sudo apt-get install python3.10 python3.10-venv

create-venv:
  {{python_executable}} -m venv venv

pip-installations:
  {{venv_executable}} -m pip install black
  {{venv_executable}} -m pip install flake8
  {{venv_executable}} -m pip install mypy

install_project:
  {{venv_executable}} -m pip install -e .

setup: apt-installations create-venv pip-installations install_project

format:
  black --line-length 120 .

lint:
  flake8 picasso
  mypy picasso