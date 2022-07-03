"""
コンテスト名から問題URLを取得する
"""

import argparse
from logging import getLogger
import pathlib
from sys import exit as exitwith
from typing import Dict

from onlinejudge.dispatch import contest_from_url
from onlinejudge_api.get_contest import main as onlinejudge_run
from requests.exceptions import HTTPError
from requests.sessions import Session

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
    parser_get_contest = subparser.add_parser(
        'get-contest', help='get problems from contest URL')
    parser_get_contest.add_argument('url', help='contest URL')
    parser_get_contest.add_argument(
        'contest_name', type=pathlib.Path, help='file name as which save')
    parser_get_contest.add_argument(
        '--config_file', type=pathlib.Path, default=CONFIG_FILE, help='config file')


def generate(url: str, session: Session) -> Dict[str, str]:
    """
    URLからコンテスト問題を取得する

    Parameters
    ----------

    url : str
        取得したいコンテストのURL
    session : Session
        ログイン情報が乗ったセッション

    Returns
    -------
    res: dict[str,str]
        問題URLの末尾とそのURLの辞書
    """

    contest = contest_from_url(url)
    try:
        contest_list = onlinejudge_run(contest, is_full=False, session=session)
    except HTTPError as error:
        logger.error(error)
        logger.error(
            'contest URL not found! \n check wheater you can login with `$ runer --login`')
        exitwith(error)
    res = {}
    for problem in contest_list["problems"]:
        res[problem["url"].split("/")[-1]] = problem["url"]
    return res
