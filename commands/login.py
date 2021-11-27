"""
ログインしたセッションを作成する
"""


import json
from getpass import getpass
from logging import getLogger

import bs4
import requests

logger = getLogger(__name__)


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


def login(url: str, config_file: str):
    """
    ログインをする

    Parameters
    ----------
    url : str
        ログインURL
    config_file : str
        ユーザー情報が乗ったファイルのパス

    Returns
    -------
    session : requests.session.Session
        ログイン後のセッション
    """
    session = requests.session()
    res = session.get(url)
    page = bs4.BeautifulSoup(res.text, 'lxml')
    csrf_token = page.find(attrs={'name': 'csrf_token'}).get('value')
    username = None
    password = None
    info=None
    try:
        with open(config_file, 'r', encoding='UTF-8') as config:
            info = json.load(config)
            username = info["user_info"]["username"]
            password = info["user_info"]["password"]
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
    session.post(url, data=login_info)
    with open(config_file, 'w', encoding='UTF-8') as config:
        info["user_info"]={"username":username,"password":password}
        json.dump(info,config,indent=4)
    return session
