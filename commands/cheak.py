"""
ファイルを実行して、検証する
"""
import argparse
from logging import getLogger
import os
from re import sub
from onlinejudge_command.subcommand.test import add_subparser as add_test 
from onlinejudge_command.main import main 
from onlinejudge_command.subcommand.test import run
from pathlib import Path
from commands.logger import logger

logger = getLogger(__name__)
def add_subparser(subparser:argparse.Action) -> None:
	""" 
	ここのサブコマンド用引数を追加する

	Parameters
	----------
	subparser : argparse.Action
		サブコマンドを格納するパーサー
	"""
	add_test(subparser)


def cheak(subparser:argparse.Namespace):
	"""
	テストケースを実行する
	"""
	subparser.command=f"./{os.path.splitext(os.path.basename(subparser.test[0]))[0]}.out"
	subparser.test.pop()
	run(subparser)
	