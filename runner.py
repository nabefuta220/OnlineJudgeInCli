#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
実行時の根幹ファイル
"""
import argparse
import json
import sys
from logging import INFO, StreamHandler, basicConfig, getLogger

from onlinejudge_command import log_formatter

from commands.bulid import add_subparser as add_build
from commands.bulid import bulid, exert
from commands.cheak import add_subparser as add_cheak
from commands.cheak import cheak
from commands.creat import add_subparser as add_creat
from commands.creat import creat
from commands.expand import add_subparser as add_expand
from commands.expand import expand
from commands.generate import add_subparser as add_gen
from commands.generate import generate
from commands.generate_template import add_subparser as add_gen_temp
from commands.generate_template import generate as gen_temp
from commands.sub_n_track import add_subparser as add_sub_n
from commands.sub_n_track import submittdNtrack
from commands.submit import add_subparser as add_sub
from commands.submit import submit
from commands.tracker import add_subparser as add_track
from commands.tracker import track

logger = getLogger(__name__)



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
    add_cheak(subparser)#test用
    add_sub(subparser)#submit用
    add_expand(subparser)#expand用
    add_track(subparser)#track用
    add_sub_n(subparser)#sub_n_track用
    return parser







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
        #複数の問題をダウンロードする
        with open(arg.file, 'r',encoding='UTF-8') as file:
            res = json.load(file)
        generate(res,arg.contest_name,arg.config_file)
    elif arg.subcommand in ['creat']:
        #環境構築を行う
        creat(arg.file,arg.url,arg.config_file)
    elif arg.subcommand in ['exe']:
        #実行する
        bulid(arg.test)
        exert(arg.test)
    elif arg.subcommand in ['test'] :
        #テストを通す
        bulid(arg.test)
        cheak(arg)
    elif arg.subcommand in ['submit']:
        #提出する
        submit(arg)
    elif arg.subcommand in ['expand']:
        #展開する
        expand(arg.file,arg.incpath)
    elif arg.subcommand in ['tracker']:
        print(track(arg.url,arg.config_file,'tmp.html'))
    elif arg.subcommand in['subntrack']:
        submittdNtrack(arg.file,arg.config_file)



def main():
    """
    呼び出し元のメソッド
    """
    level = INFO
    handler = StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter.LogFormatter())
    basicConfig(level=level, handlers=[handler])
    prase=prepara_arg()
    arg=prase.parse_args()
    tools(arg)
