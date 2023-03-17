from distutils.core import setup

setup(
    name="picasso",
    version="0.0.1",
    author="Ido Buenos",
    author_email="buenos.work@gmail.com",
    packages=["picasso"],
    install_requires=["pydantic==1.10.6"],
    extras_require={
        "dev": [
            "pytest==7.2.2",
            "isort==5.12.0",
            "black==23.1.0",
            "flake8==6.0.0",
            "mypy==1.1.1"
        ]
    }
)
