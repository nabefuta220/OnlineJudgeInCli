"""
ファイルのコンパイルと実行を行う
"""
import argparse
from logging import getLogger
import os
import subprocess

from commands.logger import logger

logger = getLogger(__name__)

def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_build = subparser.add_parser('exe')
    parser_build.add_argument('file')

def bulid(file:str):
    """
    コンパイルする
    """
    
    files=os.path.splitext(os.path.basename(file[0]))[0]
    # 拡張子に合わせて変更できようにする
    optional_cpp = "-std=gnu++17 -Wall -Wextra -O2 -DLOCAL -I /opt/ac-library"
    command = f"g++ {files}.cpp -o {files}.out {optional_cpp}"
    logger.info(command)
    res = subprocess.run(shell=True, args=command)
    if res.returncode != 0:
        exit()


def exert(file):
    """
    実行する
    """
    files=os.path.splitext(os.path.basename(file[0]))[0]
    command = f'./{files}.out'
    subprocess.run(shell=True, args=command)
