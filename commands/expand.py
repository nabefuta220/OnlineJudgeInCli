"""
cppファイル内にあるac-librayを展開する
"""
import argparse


from pathlib import Path
import subprocess
from logging import getLogger

from commands import CONFIG_FILE
from commands.json_io import get_include_path_with_ailas


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
    expander, include = get_include_path_with_ailas(ailas, config_file)
    command = f"python3 {expander} {file} --lib { include}"
    logger.info(command)
    subprocess.run(shell=True, args=command, check=True)
