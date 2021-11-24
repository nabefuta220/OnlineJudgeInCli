"""
モジュールのセットアップを行う
"""
from setuptools import setup

setup(
	name="OJC",
	version="v1.1",
	author='nabefuta220',
	install_requires=[
	   "bs4","online-judge-api-client","online-judge-tools"
	],
	entry_points={
		"console_scripts": [
		"runer = runner:main"
		]

	}
)
