import argparse
import json
import os
import subprocess
from logging import getLogger

from . import CONFIG_FILE, get_problem

logger=getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
	"""
	ここのサブコマンド用引数を追加する

	Parameters
	----------
	subparser : argparse.Action
			サブコマンドを格納するパーサー
	"""
	parser_create = subparser.add_parser('creat')
	parser_create.add_argument('file')
	parser_create.add_argument('--config_file','-c', default=CONFIG_FILE)
	parser_create.add_argument('-u', '--url')


def creat(file, url,config_file):
	os.makedirs(file)
	try:
		with open(config_file, 'r') as f:
			q = json.load(f)["preset"]
			for file_name in q.keys():
				with open(file + "/" + file_name, mode="w") as f2:
					for strings in q[file_name]:
						f2.write(strings + "\n")
				logger.info("created "+file + "/" + file_name)
				
	except FileNotFoundError as e:
		logger.error(f'configfile : {config_file} not found')

	if url :
		try:
			subprocess.run(f"cd {file} && oj d {url}", shell=True)
		except Exception as e:
			print(e)
		else:
			get_problem.get_problem(url, file+ "/"+url.split("/")[-1]+".md",config_file)


