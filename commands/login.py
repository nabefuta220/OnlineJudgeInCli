"""
ログインしたセッションを作成する
"""


import json
from logging import getLogger
import bs4
import requests

logger = getLogger(__name__)


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
    try:
        with open(config_file, 'r', encoding='UTF-8') as config:
            info = json.load(config)["user_info"]
        login_info = {
            "csrf_token": csrf_token,
            "username": info["username"],
            "password": info["password"],
        }
        session.post(url, data=login_info)
    except FileNotFoundError:
        logger.error("config file :%s not found", config_file)
    except KeyError:
        logger.error(
            "to login, key:user_info[username], user_info[password] needed in %s", config_file)
    return session
