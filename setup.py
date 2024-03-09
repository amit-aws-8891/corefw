from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="corefw",
    version="1.0.0",
    install_requires=required,
    python_requires=">=3.9",
    packages=find_packages(include=["corefw", "corefw.*"]),
)
