"""
回答環境を構築する
"""
import argparse

from os import makedirs
import subprocess
from logging import getLogger
from pathlib import Path
from requests.sessions import Session
from commands.json_io import get_config

from commands import CONFIG_FILE
from commands.get_problem import get_problem

logger = getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_create = subparser.add_parser(
        'creat', help='create coding environment')
    parser_create.add_argument(
        'file', type=Path, help='path to creat environment')
    parser_create.add_argument('--config_file', '-c', default=CONFIG_FILE)
    parser_create.add_argument('-u', '--url', type=str, help='problem URL')


def creat(file: Path, config_file: Path, session: Session, url: str = None):
    """
    問題回答環境を作成する

    Parameters
    ----------
    file : Path
        環境を作成するファイルのパス
    config_file : Path
        環境を作るための初期ファイルの情報
    session : Requests.session.Session
        ログイン情報
    url : str  (default = None)
        問題URL
    """

    makedirs(file, exist_ok=True)

    try:

        presets = get_config(config_file, "preset")
        for file_name in presets.keys():
            open_file = file/str(file_name)
            with open(open_file, encoding='UTF-8', mode="w") as out_file:
                for strings in presets[file_name]:
                    out_file.write(strings + "\n")
            logger.info("created %s/%s", file, file_name)

    except FileNotFoundError:
        logger.error('configfile : %s not found', config_file)

    if url:
        try:
            subprocess.run(
                args=f"cd {file} && oj d {url}", check=True, shell=True)
        except subprocess.CalledProcessError as ex:
            print(ex)
        finally:
            creat_file = f"{file}/{url.split('/')[-1]}.md"
            get_problem(url=url, file=creat_file,
                        session=session, config_file=config_file)
