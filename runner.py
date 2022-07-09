#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
実行時の根幹ファイル
"""
import argparse
import json
import sys
from functools import partial
from logging import INFO, StreamHandler, basicConfig, getLogger

from onlinejudge_command import log_formatter
from requests import Session

from commands import LOGIN_URL
from commands.bulid import add_subparser as add_build
from commands.bulid import bulid, exert
from commands.cheak import add_subparser as add_cheak
from commands.cheak import cheak
from commands.creat import add_subparser as add_creat
from commands.creat import creat as creat_main
from commands.expand import add_subparser as add_expand
from commands.expand import expand as expand_main
from commands.generate import add_subparser as add_gen
from commands.generate import generate as generate_main
from commands.generate_template import add_subparser as add_gen_temp
from commands.generate_template import generate as gen_temp
from commands.login import DidnotLogginedError
from commands.login import add_subparser as add_login
from commands.login import login as login_main
from commands.sub_n_track import add_subparser as add_sub_n
from commands.sub_n_track import submittd_n_track
from commands.submit import add_subparser as add_sub
from commands.submit import submit as submit_main
from commands.tracker import add_subparser as add_track
from commands.tracker import track
from commands.add_path import add_subparser as add_path
from commands.add_path import add_path as add_path_main

logger = getLogger(__name__)


def prepara_arg() -> argparse.ArgumentParser:
    """
    コマンドラインの取得の準備をする

    Returns
    -------
    parser: argparse.ArgumentParser
        コマンドラインのオブジェクト
    """
    # メインパーサーを作成する
    parser = argparse.ArgumentParser('OnlineJudgeInCli')
    # サブコマンド用のパーサーを作成する
    subparser = parser.add_subparsers(dest='subcommand')
    # 各コマンドごとのパーサを追加する
    add_gen_temp(subparser)  # generate-template用
    add_gen(subparser)  # generate 用
    add_creat(subparser)  # creat 用
    add_build(subparser)  # build 用
    add_cheak(subparser)  # test用
    add_sub(subparser)  # submit用
    add_expand(subparser)  # expand用
    add_track(subparser)  # track用
    add_sub_n(subparser)  # sub_n_track用
    add_login(subparser)  # login用
    add_path(subparser) # add_path用
    return parser


def select_tools(arg: argparse.Namespace):
    """
    使用するコマンドを選択する

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報

    Returns
    ----
    func : function
        選択された関数
    """
    print(arg.subcommand)
    # ログインする
    try:
        session = login_main(url=f"{LOGIN_URL}{arg.url}",
                             config_file=arg.config_file)
    except AttributeError:
        session = None
    funcdict = {'get-contest': partial(get_contest, session=session),
                'generate': partial(generate, session=session),
                'creat': partial(creat, session=session), 'exe': exe, 'test': test,
                'submit': submit, 'expand': expand, 'tracker': tracker, 'subntrack': subntrack,
                'login': login,'addpath':addpath}
    return funcdict[arg.subcommand]


def get_contest(arg: argparse.Namespace, session: Session):
    """
    コンテストの問題を取得し、問題をダウンロードする

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    session : Session
        ログイン情報
    """
    res = gen_temp(url=arg.url, session=session)
    generate_main(problems=res, contest_name=arg.contest_name,
                  config_file=arg.config_file, session=session)


def generate(arg: argparse.Namespace, session: Session):
    """
    複数の問題をダウンロードする

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    session : Session
        ログイン情報
    """
    with open(file=arg.file, mode='r', encoding='UTF-8') as file:
        res = json.load(file)
        generate_main(problems=res, contest_name=arg.contest_name,
                      config_file=arg.config_file, session=session)


def creat(arg: argparse.Namespace, session: Session):
    """
    環境構築を行う

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    session : Session
        ログイン情報
    """
    creat_main(file=arg.file, url=arg.url,
               config_file=arg.config_file, session=session)


def exe(arg: argparse.Namespace):
    """
    ファイルを実行する

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    bulid(arg.file,arg.config_file)
    exert(arg.file)


def test(arg: argparse.Namespace):
    """
    ファイルにローカルテストを通す

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    logger.info(arg)
    bulid(arg.test[0], arg.config_file)
    cheak(arg)


def submit(arg: argparse.Namespace):
    """
    ファイルを提出する

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    submit_main(arg)


def expand(arg: argparse.Namespace):
    """
    ファイルを展開する

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    expand_main(arg.file, arg.ailas, arg.config_file)


def tracker(arg: argparse.Namespace):
    """
    提出URLからジャッジ結果を返す

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    print(track(url=arg.url, output_file='tmp.html'))


def subntrack(arg: argparse.Namespace):
    """
    ファイルを提出し、結果を返す

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    submittd_n_track(file=arg.file)


def login(arg: argparse.Namespace):
    """
    ログインを試みる

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    try:
        login_main(url=LOGIN_URL+'https://atcoder.jp/contests/agc001/submissions/me',
                   config_file=arg.config_file, overwrite=True)
    except DidnotLogginedError:
        logger.error('Login Failed. Please retry.')
    else:
        logger.info('Sucessful Logined!')


def addpath(arg: argparse.Namespace):
    """
    インクルードパスを追加する

    Parameters
    ----------
    arg : argparse.Napespace
        コマンドラインの解析情報
    """
    logger.info(arg)
    add_path_main(arg.include_path, arg.alias, arg.config_file)


def main():
    """
    呼び出し元のメソッド
    """
    level = INFO
    handler = StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter.LogFormatter())
    basicConfig(level=level, handlers=[handler])
    prase = prepara_arg()
    arg = prase.parse_args()
    func = select_tools(arg)
    func(arg)
