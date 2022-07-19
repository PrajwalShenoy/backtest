from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

description = "A python package to run backtests on Indian Indexes CSV data"

setup(
    name = "backtest",
    version = "0.0.1",
    description = description,
    author = "Prajwal Shenoy",
    author_email = "prajwalkpshenoy@gmail.com",
    url = "https://github.com/PrajwalShenoy/backtest",
    install_requires = requirements,
)