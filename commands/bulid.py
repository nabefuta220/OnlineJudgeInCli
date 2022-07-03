"""
ファイルのコンパイルと実行を行う
"""
import argparse
from pathlib import Path
import subprocess
from logging import getLogger
import sys

logger = getLogger(__name__)

def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_build = subparser.add_parser('exe',help='run your code')
    parser_build.add_argument('file',type=Path,help='file to run')

def bulid(file:Path):
    """
    コンパイルする

    Parameters
    ----------
    file : pathlib.Pat
        コンパイルしたいファイルのパス
    """
    #ファイル名を取得
    files =file.stem
    # 拡張子に合わせて変更できようにする
    optional_cpp = "-std=gnu++17 -Wall -Wextra -O2 -DLOCAL -I /opt/ac-library"
    command = f"g++ {files}.cpp -o {files}.out {optional_cpp}"
    logger.info(command)
    res = subprocess.run(shell=True, args=command,check=True)
    if res.returncode != 0:
        sys.exit()


def exert(file: Path):
    """
    実行する

    Parameters
    ----------
    file : str
        実行したいファイルのパス
    """
    logger.info(file)
    files = file.stem
    #files=os.path.splitext(os.path.basename(file))[0]
    command = f'./{files}.out'
    subprocess.run(shell=True, args=command,check=False)
