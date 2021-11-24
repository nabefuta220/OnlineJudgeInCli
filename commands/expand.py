"""
cppファイル内にあるac-librayを展開する
"""
import argparse
import subprocess


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_get_contest = subparser.add_parser('expand')
    parser_get_contest.add_argument('file')
    parser_get_contest.add_argument(
        '--ac-libray_path', dest="incpath", default=None)


def expand(file:str, incpath:str):
    """
    ac-libaryを展開する

    Parameters
    ----------
    file : str
        展開するファイルのパス
    incpath : str
        AC-libaryへのパス
    """
    # ac-libraryのパスをjsonファイルなどで保存しておく
    command = f"python3 {incpath} {file}, --lib {incpath}"
    subprocess.run(shell=True, args=command,check=True)
