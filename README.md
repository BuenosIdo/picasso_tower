# Picasso Tower

Ido Buenos code for picasso tower exercise

### Environment
Python 3.10
Written on ubuntu 22.04.2 LTS

### Setup
To use the just file download just with:
```shell
sudo snap install --edge just --classic
```
To setup project:
```shell
just setup
```

### Development
To format the code with isort and black:
```shell
just format
```
To run flake8 and mypy linters on the code:
```shell
just lint
```
To run tests:
```shell
just test
```