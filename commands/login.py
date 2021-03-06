"""
ログインしたセッションを作成する
"""


import argparse
import re
from getpass import getpass
from logging import getLogger
from pathlib import Path
from urllib.request import Request

import bs4
import requests

from commands import CONFIG_FILE
from commands.json_io import get_config, write_config

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
                              type=Path, default=CONFIG_FILE, help='store login info')


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


def login(url: Request, config_file: Path, overwrite: bool = False):
    """
    ログインをする

    Parameters
    ----------
    url: urllib.request.Request
        ログインURL
    config_file: pathlib.Path
        ユーザー情報が乗ったファイルのパス
    overwrite: bool (default  False)
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
        if overwrite:
            username, password = ask_user()
        info = get_config(config_file, "user_info")
        username = info["username"]
        password = info["password"]

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

    if not responce.ok or not det_logined(responce.text, username):
        raise DidnotLogginedError(url)
    info = {"username": username, "password": password}
    write_config(config_file, "user_info", info)

    return session


def det_logined(text: str, user: str):
    """
    ログインできたかを判断する

    Parameters
    ----------
    text : str
        ログイン後のhttpソース
    user : str
        ログインしようとしているユーザー名

    Returns
    ------
    logined : textに"Welcome, {user}."が含まれればTrue,そうでなければFalse
    """
    target = f'Welcome, {str(user)}.'
    res = re.search(target, text)
    return res is not None


class DidnotLogginedError(Exception):
    """
    ログインに失敗したときに出される例外
    """

    def __init__(self, errURL):
        """
        エラーメッセージを表示する

        Parameters
        ----------

        errURL : string
            エラーの原因となったURL
        """
        message = f"""
         did not logined at {errURL}. 
         check if this URL exist or check you can logined with $ runer login."""
        super().__init__(message)
