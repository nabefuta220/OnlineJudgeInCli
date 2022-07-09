"""
ファイルのコンパイルと実行を行う
"""
import argparse
import json
from os.path import dirname
from pathlib import Path
import subprocess
from logging import getLogger
import sys


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
    parser_build = subparser.add_parser('exe', help='run your code')
    parser_build.add_argument('file', type=Path, help='file to run')
    parser_build.add_argument('--config_file', '-c',
                              type=Path, default=CONFIG_FILE, help='store include path info')


def get_include_path_list(config_file: Path):
    """
    現在のインクルードパスのリストを取得する

    Parameters
    ----------
    config_file : pathlib.Path
        インクルードファイルのパス
    Returns
    -------
    include_path_list : [str]
        インクルードパスのリスト(ディレクトリで返す)
    """
    res = []
    try:
        with open(config_file, 'r', encoding='UTF-8') as config:
            info = json.load(config)["includePath"]
            res = [dirname(value) if key != "" else value for key,
                   value in info.items()]
    except FileNotFoundError:
        pass
    except KeyError:
        pass
    return res


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
    # TODO:拡張子に合わせて変更できようにする
    include_list = " ".join(get_include_path_list(config_file))
    optional_cpp = f"-std=gnu++17 -Wall -Wextra -O2 -DLOCAL -I {include_list}"
    command = f"g++ {files}.cpp -o {files}.out {optional_cpp}"
    logger.info(command)
    res = subprocess.run(shell=True, args=command, check=True)
    if res.returncode != 0:
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
    # files=os.path.splitext(os.path.basename(file))[0]
    command = f'./{files}.out'
    subprocess.run(shell=True, args=command, check=False)
