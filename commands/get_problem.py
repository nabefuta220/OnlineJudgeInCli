from commands import THIS_MODULE
import requests
import bs4
import re
import argparse
import os
import sys
import json
from . import THIS_MODULE

from .logger import logger

LOGIN_URL = "https://atcoder.jp/login?continue="


def input():
	arg = argparse.ArgumentParser('get_problem')
	arg.add_argument('url', help="取得する問題")
	arg.add_argument('file', help="保存先")
	arg.add_argument('config_file', help="設定ファイルの場所")
	res = arg.parse_args()
	return [res.url, res.file, res.config_file]


def get_html(url, file, session,force_rewrite=False):
	if os.path.isfile(file) and not force_rewrite:
		logger.info(f"file: {file} is already exist")
	else:
		try:
			with open(file, 'w') as f:
				source = session.get(url)
				source.raise_for_status()
				soup = bs4.BeautifulSoup(source.text, "html.parser")
				f.write(str(soup))
		except requests.exceptions.HTTPError as e:
			logger.error(e)
			os.remove(file)
			exit()
		logger.debug(f"saved {url} as {file}")


def parse(infile, outfile):
	try:
		with open(infile, 'r') as f:
			soup = bs4.BeautifulSoup(f, "html.parser")
		# print(soup.title.text)
		# print(re.search(r'Time Limit: \d+ sec / Memory Limit: \d+ MB',str(soup)).group())

		chose = soup.select('.lang-ja')
		if (chose == []):
			logger.error("class leng-ja not found")
			chose = soup.select('#task-statement')
			if (chose == []):
				logger.error("id task-statement not found")
				exit()
		string = ""
		try:
			string = "# " + soup.title.text + "\n\n"
		except AttributeError as e:
			logger.error("tag<title> not found")
		try:

			string += re.search(r'Time Limit: \d+ sec / Memory Limit: \d+ MB',
								str(soup)).group()
		except AttributeError as e:
			logger.info("Time Limit and Memory Limit not found")

		string += "\n\n" + re.sub(r'\n(\s)+', '', str(chose[0]))

		# print(string)
		# Time Limit: 2 sec / Memory Limit: 1024 MB

		# string = re.sub(r'\n(\s)*', '', string)
		string = re.sub(r'<var>(\s|)*', '$', string)
		# string=string.replace("<var>",'$',-1)
		string = re.sub(r"(\s|)</var>", '$', string)
		string = string.replace("</font>", '</font>\n ', -1)
		string = string.replace("<h3>", '### ', -1)
		string = string.replace("</h3>", '\n\n', -1)
		string = string.replace("</div>", '\n\n', -1)
		string = re.sub(r'<span class=".*">', '\n\n', string)
		string = string.replace("</span>", '', -1)
		string = re.sub(r'<div class=".*">', '\n\n', string)
		string = string.replace("<p>", '', -1)
		string = string.replace("</p>", '\n\n', -1)
		string = string.replace("<section>", '', -1)
		string = string.replace("</section>", '\n\n', -1)
		string = re.sub(r'<li>(\s|)+', '<li>', string)
		string = string.replace("<ol>", '', -1)
		string = string.replace("</ol>", '\n', -1)
		string = string.replace("<ul>", '', -1)
		string = string.replace("</ul>", '\n', -1)
		string = string.replace("<li>", '- ', -1)
		string = re.sub(r"(~\n)</li>", '$1\n', string)
		string = string.replace("</li>", '', -1)
		string = string.replace("<strong>", '**', -1)
		string = string.replace("</strong>", '**', -1)
		string = string.replace("<hr/>", '----', -1)
		string = string.replace("<br/>", '', -1)
		string = string.replace("<code>", '`', -1)
		string = string.replace("</code>", '`', -1)
		string = re.sub(r'\n\n+', '\n\n', string)
		string = re.sub(r'<pre class=".*">', '<pre>', string)
		string = string.replace("\n</pre>", '</pre>', -1)
		string = string.replace("</pre>", '\n```', -1)

		string = string.replace("<pre>", '```text\n', -1)
		# string = re.sub(r'```text([^\s])', '```text\n $1', string)
		# string = string.replace('```text[^\n]', '```text\n', -1)
		string = string.replace("&lt;", '<', -1)
		string = string.replace("&gt;", '>', -1)
		try:
			with open(outfile, 'w') as f:
				f.write(string)
				logger.info(f"downloded problem as {outfile}")
		except IsADirectoryError:
			logger.error(f'file {outfile} is not file ...')
	except FileExistsError as e:
		logger.error(e)


def login(url, config_file):
	session = requests.session()
	# print(url)
	res = session.get(url)
	# print(res.text)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	csrf_token = page.find(attrs={'name': 'csrf_token'}).get('value')
	try:
		with open(config_file, 'r') as f:
			q = json.load(f)["user_info"]
		login_info = {
			"csrf_token": csrf_token,
			"username": q["username"],
			"password": q["password"],
		}
		ans = session.post(url, data=login_info)
	except FileNotFoundError as e:
		logger.error(f"config file :{config_file} not found")
	except KeyError as e:
			logger.error(f"to login, key:user_info[username], user_info[password] needed in  {config_file}")
	return session


def get_problem(url, file,config_file):
	
	session=login(LOGIN_URL+url, config_file)

	get_html(url, file+'_tmp.html', session)
	parse(file+'_tmp.html',file)
	# run(url, file, session)


if __name__ == "__main__":
	# parse("tmp.html", "b.md")
	# exit()
	url, file ,config_file= input()
	get_problem(url, file,config_file)
