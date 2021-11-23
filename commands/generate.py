"""
複数の問題の回答環境を作成する
"""
import argparse
from logging import getLogger

from commands import CONFIG_FILE
from commands.creat import creat

logger = getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_generate = subparser.add_parser('generate')
    parser_generate.add_argument('file')
    parser_generate.add_argument('contest_name')
    parser_generate.add_argument('--config_file', default=CONFIG_FILE)


def generate(problems: dict[str, str], contest_name: str, config_file: str):
    """
    コンテスト名と問題名、URLを読み込み、コンテスト名のディレクトリに回答用環境をいれる

    Parameters
    ----------
    problems:dict[str,str]
            問題名とそのURLの辞書
    contest_name:str
            保存するファイル名
    config_file :str
            設定ファイルのパス(ファイルの初期化に使用)
    """

    for folder, url in problems.items():
        creat(f"{contest_name}/{folder}", url, config_file)
