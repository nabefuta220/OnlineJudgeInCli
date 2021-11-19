from setuptools import setup

setup(
    name="OJC",
    version="alpha",
    author='nabefuta220',
    install_requires=[],
    entry_points={
        "console_scripts": [
        "acGUI = commands.main:main"
        ]
        
    }
)