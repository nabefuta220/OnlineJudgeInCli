"""
インクルードパスを追加・確認する
"""


import argparse
import json
from pathlib import Path
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
    parser_add = subparser.add_parser(
        'addpath', help='add include path')
    parser_add.add_argument('--include_path', '-p',
                            type=Path, help='file or directory to add')
    parser_add.add_argument('--alias', '-a', type=str, default='',
                            help='name to point this include path (use expand command)')
    parser_add.add_argument('--config_file', '-c',
                            type=Path, default=CONFIG_FILE, help='store login info')


def add_path(new_path: Path, ailas: str, config_file: Path):
    """
    インクルードパスを追加する

    Parameters
    ----------
    new_path : pathlib.Path
        新しく追加するヘッダーファイルの場所
    ailas : str
        ヘッダーファイルの別名
    config_file : pathlib.Path
        インクルードパスをまとめたファイル
    -------
    success : bool
        パスの追加が成功したか(すればTrue)
    """

    # 引数のパスが存在するか調べる
    new_path = new_path.resolve()
    if new_path.exists():
        logger.info('%s is exist path', new_path)
    else:
        logger.error('%s is not exist! check your path', new_path)
        sys.exit(1)

    # 設定を読み込む
    try:
        with open(config_file, 'r', encoding='UTF-8') as config:
            info = json.load(config)

    except FileNotFoundError:
        with open(config_file, 'w', encoding='UTF-8'):
            pass

    with open(config_file, 'w', encoding='UTF-8') as config:
        info.setdefault("includePath",{})

        info["includePath"][ailas]= str(new_path)
        json.dump(info, config, indent=4)
        logger.info('add %s ad ailas : %s',new_path,ailas)
