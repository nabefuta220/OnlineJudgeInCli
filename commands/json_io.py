"""
JSONから値を読み書きを行う関数を実装する
"""


from json import load, dump
from pathlib import Path
from os.path import dirname
from typing import Any


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

    Exceptions
    KeyError:
        そのような属性がなかった時
    """

    with open(config_file, 'r', encoding='UTF-8') as config:
        return load(config)[key]


def write_config(config_file: Path, key: str, value: Any):
    """
    config fileから特定の値を更新する

    Parameters
    ----------
    config_file : pathlib.Path
        config fileのパス
    key : str
        書き込みたい属性
    value: Any
        書き込みたい値
    """
    with open(config_file, 'r', encoding='UTF-8') as config:
        data = load(config)
    data.setdefault(key, {})
    data[key] |= value
    with open(config_file, 'w', encoding='UTF-8') as config:
        dump(data, config, indent=4)


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
            info = load(config)["includePath"]
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
    expand_path = get_config(config_file, "includePath")[ailas]
    include_path = dirname(expand_path)
    return (expand_path, include_path)
