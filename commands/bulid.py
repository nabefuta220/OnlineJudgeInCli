"""
ファイルのコンパイルと実行を行う
"""
import argparse
import subprocess
import sys
from logging import getLogger
from pathlib import Path

from commands import CONFIG_FILE
from commands.json_io import get_include_path_list

logger = getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_build = subparser.add_parser('exe', help='run your code')
    parser_build.add_argument('file', type=Path, help='file to run')
    parser_build.add_argument('--config_file', '-c',
                              type=Path, default=CONFIG_FILE, help='store include path info')


def bulid(file: Path, config_file: Path):
    """
    コンパイルする

    Parameters
    ----------
    file : pathlib.Path
        コンパイルしたいファイルのパス
    config_file : pathlib.Path
        インクルードファイルのパス
    """
    # ファイル名を取得
    files = file.stem
    include_list = " -I ".join(get_include_path_list(config_file))
    optional_cpp = f"-std=gnu++17 -Wall -Wextra -O2 -DLOCAL -I {include_list}"
    command = f"g++ {files}.cpp -o {files}.out {optional_cpp}"
    logger.info(command)
    try:
        subprocess.run(shell=True, args=command, check=True)
    except subprocess.CalledProcessError as error:
        logger.error("build finished with returncode %s.",(error.returncode))
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
    command = f'./{files}.out'
    try:
        subprocess.run(shell=True, args=command, check=False)
    except KeyboardInterrupt:
        print()
        logger.error("KeyboardInterrupted")
