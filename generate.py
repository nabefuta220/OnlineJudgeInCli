import creat
import json

from logger import logger


def generate(config_file):
	try:
		with open(config_file, 'r') as f:
			q = json.load(f)["query"]
		for folder, url in q.items():
			creat.creat(folder, url, config_file)
	except FileNotFoundError:
		logger.error(f"config file: {config_file} not found")
	except KeyError:
		logger.error(f"key: ['query'] in config file: {config_file} not found")

if __name__ == '__main__':
	generate('config.json')