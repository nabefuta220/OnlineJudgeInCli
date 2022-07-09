"""
cppファイル内にあるac-librayを展開する
"""
import argparse

import json
from pathlib import Path
import subprocess
from logging import getLogger
from os.path import dirname

from commands import CONFIG_FILE


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
    parser_get_contest.add_argument('ailas',
                                    type=str, help='ailas of include path')
    parser_get_contest.add_argument('--config_file', '-c',
                                    type=Path, default=CONFIG_FILE, help='store include path info')


def expand(file: Path, ailas: str, config_file: Path):
    """
    ヘッダーファイルを展開する

    Parameters
    ----------
    file : Path
        展開するファイルのパス
    ailas : str
        展開ファイル用パスへの別名
    config_file : pathlib.Path
        インクルードパスをまとめたファイル
    """
    expand, include = get_include_path_with_ailas(ailas, config_file)
    #TODO: ac-libraryのパスをjsonファイルなどで保存しておく
    command = f"python3 {expand} {file} --lib { include}"
    logger.info(command)
    subprocess.run(shell=True, args=command, check=True)


#TODO : config_fileからデータを読み込む系の関数を別ファイルに実装する
def get_include_path_with_ailas(ailas: str, config_file: Path):
    """
    ヘッダーファイルへのパスを別名から取得する
    Parameters
    ----------
    ailas : str
        展開ファイル用パスへの別名
    config_file : pathlib.Path
        インクルードパスをまとめたファイル

    Returns
    -------
    expand_file : str
        展開用ファイルへのパス
    include_path : str
        ヘッダーファイルへのパス
    """

    with open(config_file, 'r', encoding='UTF-8') as config:
        info = json.load(config)["includePath"]
        expand_path = info[ailas]
        include_path = dirname(expand_path)
    return (expand_path, include_path)
