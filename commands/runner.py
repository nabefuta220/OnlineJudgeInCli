#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import argparse
import json
import subprocess
import sys
from logging import INFO, StreamHandler, basicConfig, getLogger
from re import template

import onlinejudge_command.log_formatter as log_formatter

from commands.bulid import add_subparser as add_build
from commands.bulid import bulid, exert
from commands.cheak import add_subparser as add_cheak
from commands.cheak import cheak
from commands.generate import generate

from .cheak import add_subparser as add_test
from .creat import add_subparser as add_creat
from .creat import creat
from .generate import add_subparser as add_gen
from .generateTemplate import add_subparser as add_gen_temp
from .generateTemplate import generate as gen_temp

cxxflag = '-std=gnu++17 -Wall -Wextra -O2'
oj_testflag = ''

home = '/home/nabefuta/atcoder'

sys.path.append(home)
logger = getLogger(__name__)

if '/home/nabefuta/atcoder' in sys.path:
	from . import tracker

def prepara_arg()->argparse.ArgumentParser:
	"""
	コマンドラインの取得の準備をする

	Returns
	-------
	parser: argparse.ArgumentParser
		コマンドラインのオブジェクト
	"""
	#メインパーサーを作成する
	parser=argparse.ArgumentParser('tools')
	#サブコマンド用のパーサーを作成する
	subparser=parser.add_subparsers(dest='subcommand')
	#各コマンドごとのパーサを追加する
	add_gen_temp(subparser)#generate-template用
	add_gen(subparser)#generate 用
	add_creat(subparser)#creat 用
	add_build(subparser)#build 用
	add_cheak(subparser)#cheak用
	add_test(subparser)#test用
	
	return parser

def input_arg():
	"""
	コマンドラインからの入力を受け付ける
	"""
	parse = argparse.ArgumentParser('tools')
	parse.add_argument('mode', choices=[
					   'test', 'cheak', 'sub', 'track', 'init', 'subntrack', 'expand', 'get-contest'])
	parse.add_argument('-u', '--URL', default='test', help='問題URL,もしくは提出結果のURL')
	parse.add_argument(
		'--incdir', default='-I /home/nabefuta/atcoder/ac-library', help='at-llibaryのパス')

	parse.add_argument('--target', default='Main', help='ソースファイル')
	parse.add_argument('--cxx', default='g++', help='c++のコンパイラ')

	args = parse.parse_args()

	dict = {'mode': args.mode, 'url': args.URL, 'incdir': args.incdir,
		'target': args.target, 'cxx': args.cxx, 'oj_testflag': oj_testflag, 'cxxflag': cxxflag}
	return dict


def submitte(target):
	"""
	提出する
	"""
	command = 'oj s %s --no-open' % (target)
	subprocess.run(shell=True, args=command)


def init(url):
	"""
	テストケースを取得する
	"""
	command = 'oj d %s' % (url)
	subprocess.run(shell=True, args=command)


def expand(target):
	"""
	ac-libaryを展開する
	"""
	command = 'python %s %s --lib %s' % (home +
										 '/ac-library/expander.py', target, home+'/ac-library/')
	subprocess.run(shell=True, args=command)


def submittdNtrack(target):
	"""
	提出して、結果を見る
	"""
	command = 'oj s %s --no-open -y | python %s %s' % (
		target, home+'/sub_n_track.py', home+'/config.json')
	subprocess.run(shell=True, args=command)


def tools(arg:argparse.Namespace):
	"""
	コマンドを実行する
	"""
	print(arg.subcommand)
	if arg.subcommand in ['get-contest']:
		#コンテストの問題を取得し、問題をダウンロードする
		res=gen_temp(arg.url)
		generate(res,arg.contest_name,arg.config_file)
	elif arg.subcommand in ['generate']:
		#問題をダウンロードする
		with open(arg.file, 'r') as f:
			res = json.load(f)
		generate(res,arg.contest_name,arg.config_file)
	elif arg.subcommand in ['creat']:
		creat(arg.file,arg.url,arg.config_file)
	elif arg.subcommand in ['exe']:
		bulid(arg.test)
		exert(arg.test)
	elif arg.subcommand in ['test'] :
		bulid(arg.test)
		cheak(arg)
	elif mode == 'sub':
		submitte(arg['target']+'.cpp')
	elif mode == 'init':
		init(arg['url'])
	elif mode == 'track':
		print(tracker.track(arg['url'], home+'/config.json', 'tmp.html'))
	elif mode == 'subntrack':
		submittdNtrack(arg['target']+'.cpp')
	elif mode == 'expand':
		expand(arg['target']+'.cpp')


def main():
	level = INFO
	handler = StreamHandler(sys.stdout)
	handler.setFormatter(log_formatter.LogFormatter())
	basicConfig(level=level, handlers=[handler])
	prase=prepara_arg()
	arg=prase.parse_args()
	tools(arg)
