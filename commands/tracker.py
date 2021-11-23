from logging import getLogger


logger=getLogger(__name__)

from .get_problem import login, get_html, LOGIN_URL
import time
import requests
import bs4
import os
import re

import argparse

def parse(file):
	res={}
	try:
		with open(file, 'r') as f:
			soup = bs4.BeautifulSoup(f, "html.parser")
		matchobj = re.search(
			r'<tr>\n<th>Score</th>\n<td .*/td>\n</tr>', str(soup.html))
		if matchobj:
			res["score"] = matchobj.group()
			matchobj = re.search(
				r'<tr>\n<th .*>Submission Time</th>\n<td class="text-center"><time .*</time></td>\n</tr>', str(soup.html))
		if matchobj:
			res["time"] = matchobj.group()
		chose = soup.select('#judge-status')
		res["state"]=chose[0].text
	except Exception as e:
		logger.error(e)
		return None

	return (res)


def input():
	arg = argparse.ArgumentParser('tracker')
	arg.add_argument('url', help="取得する問題")
	arg.add_argument('config', help="設定ファイル")
	res = arg.parse_args()
	return {"url":res.url,"config":res.config}

def track(url,config_file,output_file):
	session = login(LOGIN_URL+url, config_file)
	res = {}
	
	for i in range(1, 300):
		get_html(url, output_file , session, True)
		res = parse(output_file)
		state = ""

		matchobj = re.search(r'[A-Z]+', res["state"])
		if matchobj:
			state = matchobj.group()

		if not state in ["WJ", "WR", ""]:
			logger.info("done!")
			matchobj2 = re.search(r'\d+', res["score"])
			matchobj3 = re.search(
				r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{4}', res["time"])
			res['time'] = matchobj3.group()
			res['score'] = matchobj2.group()
			res['state'] = state
			res['url'] = url
		
			return res
		else:
			logger.info("proceeding ... ( " + res["state"]+")")
		time.sleep(1)
	logger.info("terminate due to long time taken")
	return None


if __name__ == "__main__":
	res=input()



	print(track(res['url'], res['config'], 'tmp.html'))

