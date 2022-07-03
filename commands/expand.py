"""
cppファイル内にあるac-librayを展開する
"""
import argparse
from pathlib import Path
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
        'file', type=Path, help='file to expand')
    parser_get_contest.add_argument(
        '--ac-libray_path', dest="incpath", type=Path, default="", help='include path')


def expand(file:Path, incpath: Path):
    """
    ac-libaryを展開する

    Parameters
    ----------
    file : Path
        展開するファイルのパス
    incpath : Path
        AC-libaryへのパス
    """
    # ac-libraryのパスをjsonファイルなどで保存しておく
    command = f"python3 {incpath}/expander.py {file} --lib {incpath}"
    logger.info(command)
    subprocess.run(shell=True, args=command, check=True)
