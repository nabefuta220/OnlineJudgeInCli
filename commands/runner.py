#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from re import template
import sys
import subprocess
import argparse
from .generateTemplate import generate as gen_temp
cxxflag = '-std=gnu++17 -Wall -Wextra -O2'
oj_testflag = ''

home = '/home/nabefuta/atcoder'

sys.path.append(home)

if '/home/nabefuta/atcoder' in sys.path:
	from .import tracker


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
	parse.add_argument('--cxx', default='g++', help='c++のコンパイラ', )

	args = parse.parse_args()

	dict = {'mode': args.mode, 'url': args.URL, 'incdir': args.incdir,
		'target': args.target, 'cxx': args.cxx, 'oj_testflag': oj_testflag, 'cxxflag': cxxflag}
	return dict


def bulid(cxx, cxxflag,  incdir, target, macro=''):
	"""
	コンパイルする
	"""
	command = '%s %s %s %s -o %s %s' % (cxx, cxxflag,
										macro, incdir, target+'.out', target+'.cpp')
	res = subprocess.run(shell=True, args=command)
	if res.returncode != 0:
		exit()


def exert(target):
	"""
	実行する
	"""
	command = './%s.out' % (target)
	subprocess.run(shell=True, args=command)


def cheak(oj_testflag, target):
	"""
	テストケースを実行する
	"""
	command = 'oj t -N -S %s -c %s' % (oj_testflag, './' + target)
	subprocess.run(shell=True, args=command)


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


def tools(arg: dict):
	"""
	コマンドを実行する
	"""
	mode = arg['mode']
	if mode == 'test':
		bulid(arg['cxx'], arg['cxxflag'], arg['incdir'], arg['target'], '-DLOCAL')
		exert(arg['target'])
	elif mode == 'cheak':
		bulid(arg['cxx'], arg['cxxflag'], arg['incdir'],
			  arg['target'], '-DONLINE_JUDGE')
		cheak(arg['oj_testflag'], arg['target']+'.out')
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
	elif mode == 'get-contest':
		#コンテストの問題を取得する
		res=gen_temp(arg['url'])
		print(res)

def main():
	arg = input_arg()
	tools(arg)
