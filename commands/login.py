"""
ログインしたセッションを作成する
"""


import argparse
import json
import pathlib
from getpass import getpass
from logging import getLogger

import bs4
import requests

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
    parser_login = subparser.add_parser(
        'login', help='login to atcoder')
    parser_login.add_argument('--config_file', '-c',
                              type=pathlib.Path, default=CONFIG_FILE, help='store login info')


def ask_user():
    """
    ユーザー名とパスワードを尋ねる

    Returns
    -------
    user : str
        ユーザー名
    password :str
        パスワード
    """
    user = input("user:")
    password = getpass()
    return user, password


def login(url: str, config_file: str, overwrite: bool = False):
    """
    ログインをする

    Parameters
    ----------
    url: str
        ログインURL
    config_file: str
        ユーザー情報が乗ったファイルのパス
    overwrite: bool(befault=False)
        強制的にユーザー名とパスワードを尋ねる
    Returns
    -------
    session: requests.session.Session
        ログイン後のセッション
    """
    session = requests.session()
    res = session.get(url)
    page = bs4.BeautifulSoup(res.text, 'lxml')
    csrf_token = page.find(attrs={'name': 'csrf_token'}).get('value')
    username = None
    password = None
    info = None
    try:
        with open(config_file, 'r', encoding='UTF-8') as config:
            info = json.load(config)
            username = info["user_info"]["username"]
            password = info["user_info"]["password"]
            if overwrite:
                username, password = ask_user()
    except FileNotFoundError:
        logger.error("config file :%s not found", config_file)
        with open(config_file, 'w', encoding='UTF-8'):
            pass
        username, password = ask_user()
    except KeyError:
        username, password = ask_user()
    login_info = {
        "csrf_token": csrf_token,
        "username": username,
        "password": password,
    }
    responce = session.post(url, data=login_info)
    if not responce.ok:
        raise DidnotLogginedError(url)
    with open(config_file, 'w', encoding='UTF-8') as config:
        info["user_info"] = {"username": username, "password": password}
        json.dump(info, config, indent=4)
    return session


class DidnotLogginedError(Exception):
    """
    ログインに失敗したときに出される例外
    """

    def __init__(self, errURL):
        message = f"""
         did not logined at {errURL}. 
         check if this URL exist or check you can logined with $ runer login."""
        super().__init__(message)
