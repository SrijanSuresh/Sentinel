from setuptools import setup, find_packages

setup(
name="sentinel",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "sentinel=main:main",
        ],
    },
)

