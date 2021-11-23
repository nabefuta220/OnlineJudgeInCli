import argparse
import subprocess
import sys
from logging import INFO, StreamHandler, basicConfig, getLogger

import onlinejudge_command.log_formatter as log_formatter

from commands import CONFIG_FILE, THIS_MODULE, submittgetter, tracker

logger=getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_sub_n_track = subparser.add_parser('subntrack')
    parser_sub_n_track.add_argument('file')
    parser_sub_n_track.add_argument('--config_file', default=CONFIG_FILE)

def input():
	arg = argparse.ArgumentParser("sub & track")
	arg.add_argument("config")
	parse = arg.parse_args()

	return {"config": parse.config, "url": submittgetter.get_submittion_URL(submittgetter.get_data())}



def submittdNtrack(file,config_file):
	"""
	提出して、結果を見る
	"""
	
	tmp_file=f"{THIS_MODULE}/../res.tmp"
	with open(tmp_file,'w'):
		pass
	command = f'oj s {file} --no-open -y >> {tmp_file}'
	subprocess.run(shell=True, args=command)
	with open(tmp_file,'r')as f:
		str=f.read()
		print(str)

	url=submittgetter.get_submittion_URL(str)
	
	print(tracker.track(url,config_file,'tmp.html'))




if __name__ == "__main__":
	
	level = INFO
	handler = StreamHandler(sys.stdout)
	handler.setFormatter(log_formatter.LogFormatter())
	basicConfig(level=level, handlers=[handler])
	res = input()
	print(tracker.track(res['url'], res['config'], "tmp.html"))
	
