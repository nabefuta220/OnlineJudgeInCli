
from setuptools import setup

setup(
    name="OJC",
    version="alpha",
    author='nabefuta220',
    install_requires=[
       "bs4","online-judge-api-client"
    ],
    entry_points={
        "console_scripts": [
        "acGUI = commands.main:main",
        "runer = commands.runner:main"
        ]
        
    }
)