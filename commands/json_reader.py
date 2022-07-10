"""
JSONから値を読み込む関数を実装する
"""


import json
from pathlib import Path
from os.path import dirname


def get_config(config_file: Path, key: str):
    """
    config fileから特定の変数を取り出す

    Parameters
    ----------
    config_file : pathlib.Path
        config fileのパス
    key : str
        取り出したい値
    Returns
    -------
    value : Any
        config fileのパスのkeyの値
    """
    with open(config_file, 'r', encoding='UTF-8') as config:
        return json.load(config)[key]


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
    expand_path=get_config(config_file,"includePath")[ailas]
    include_path = dirname(expand_path)
    return (expand_path, include_path)
