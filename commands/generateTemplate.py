
from onlinejudge_api.get_contest import main as onlinejudge_run
from .logger import logger
import onlinejudge.dispatch as dispatch

def generate(url):

	contest=dispatch.contest_from_url(url)

	str=onlinejudge_run(contest,is_full=False,session='')
	pro=str['problems']

	for i in pro:
		print(i["url"],i["url"].split("/")[-1])
	

