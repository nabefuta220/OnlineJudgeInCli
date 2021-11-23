import argparse
import os
from logging import getLogger

from onlinejudge.utils import default_cookie_path
from onlinejudge_command.subcommand.submit import add_subparser as add_sub
from onlinejudge_command.subcommand.submit import run

logger = getLogger(__name__)

def add_subparser(subparser:argparse.Action) -> None:
	""" 
	ここのサブコマンド用引数を追加する

	Parameters
	----------
	subparser : argparse.Action
		サブコマンドを格納するパーサー
	"""
	add_sub(subparser)


def submit(subparser:argparse.Namespace):
	"""
	提出する
	"""
	subparser.cookie=default_cookie_path
	subparser.open=False
	print(subparser)
	run(subparser)
