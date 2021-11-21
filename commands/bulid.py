"""
ファイルのコンパイルと実行を行う
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
    parser_build = subparser.add_parser('test')
    parser_build.add_argument('file')

def bulid(file):
    """
    コンパイルする
    """
    # 拡張子に合わせて変更できようにする
    optional_cpp = "-std=gnu++17 -Wall -Wextra -O2 -DLOCAL -I /opt/ac-library"
    command = f"g++ {file}.cpp -o {file}.out {optional_cpp}"
    res = subprocess.run(shell=True, args=command)
    if res.returncode != 0:
        exit()


def exert(file):
    """
    実行する
    """
    command = f'./{file}.out'
    subprocess.run(shell=True, args=command)
