import argparse
import subprocess
from . import get_problem
import json

from .logger import logger
def input():
	parse = argparse.ArgumentParser('creat')
	parse.add_argument('file')
	parse.add_argument('config_file')
	parse.add_argument('-u', '--URL')
	args = parse.parse_args()
	return {'file': args.file, 'url': args.URL, 'config_file': args.config_file}


def creat(file, url,config_file):
	subprocess.run("mkdir -p " + file, shell=True)
	try:
		with open(config_file, 'r') as f:
			q = json.load(f)["preset"]
			for file_name in q.keys():
				with open(file + "/" + file_name, mode="w") as f2:
					for strings in q[file_name]:
						f2.write(strings + "\n")
				logger.info("created "+file + "/" + file_name)
				if file_name=='tools':
					subprocess.run(shell=True, args='chmod u+x %s' % (file + "/" + file_name))
					logger.info(f"gave permission (exe) in {file}/{file_name}")
	except FileNotFoundError as e:
		logger.error(f'configfile : {config_file} not found')

	if url != None and url != "":
		try:
			subprocess.run("cd " + file + " && oj d " + url, shell=True)
		except Exception as e:
			print(e)
		else:
			get_problem.get_problem(url, file+ "/"+url.split("/")[-1]+".md",config_file)


if __name__ == "__main__":
	res = input()
	creat(res['file'], res['url'], res['config_file'])
