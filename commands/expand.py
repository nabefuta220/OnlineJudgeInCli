"""
cppファイル内にあるac-librayを展開する
"""
import argparse
import pathlib
import subprocess
from logging import getLogger


logger = getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_get_contest = subparser.add_parser(
        'expand', help='expand AC libray')
    parser_get_contest.add_argument(
        'file', type=pathlib.Path, help='file to expand')
    parser_get_contest.add_argument(
        '--ac-libray_path', dest="incpath", type=pathlib.Path, default="", help='include path')


def expand(file: pathlib.Path, incpath: pathlib.Path):
    """
    ac-libaryを展開する

    Parameters
    ----------
    file : pathlib.Path
        展開するファイルのパス
    incpath : pathlib.Path
        AC-libaryへのパス
    """
    # ac-libraryのパスをjsonファイルなどで保存しておく
    command = f"python3 {incpath}/expander.py {file} --lib {incpath}"
    logger.info(command)
    subprocess.run(shell=True, args=command, check=True)
