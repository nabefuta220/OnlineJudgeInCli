"""
複数の問題の回答環境を作成する
"""
import argparse
from logging import getLogger
from pathlib import Path
from typing import Dict
from urllib.request import Request

from requests.sessions import Session

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
    parser_generate = subparser.add_parser('generate',
                                           help='generate template in multiplie problems')
    parser_generate.add_argument('file', type=Path,
                                 help='jsonfile contained dictionary of prblem ID and problem URL')
    parser_generate.add_argument('contest_name', type=Path, help='constest name')
    parser_generate.add_argument(
        '--config_file', type=Path, default=CONFIG_FILE, help='config file')


def generate(problems: Dict[str, Request], contest_name: Path, config_file: Path, session: Session):
    """
    コンテスト名と問題名、URLを読み込み、コンテスト名のディレクトリに回答用環境をいれる

    Parameters
    ----------
    problems:dict[str,urllib.request.Request]
        問題名とそのURLの辞書
    contest_name: Path
        保存するファイル名
    config_file : Path
        設定ファイルのパス(ファイルの初期化に使用)
    session : requests.sessions.Session
        ログイン情報
    """

    for folder, url in problems.items():
        creat(file=f"{contest_name}/{folder}", url=url,
                   config_file=config_file, session=session)
