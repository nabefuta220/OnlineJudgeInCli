"""
コンテスト名から問題URLを取得する
"""

import argparse
from logging import getLogger
from typing import Dict
from onlinejudge.dispatch import contest_from_url


from onlinejudge_api.get_contest import main as onlinejudge_run

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
    parser_get_contest = subparser.add_parser('get-contest')
    parser_get_contest.add_argument('url')
    parser_get_contest.add_argument('contest_name')
    parser_get_contest.add_argument('--config_file', default=CONFIG_FILE)


def generate(url: str) -> Dict[str, str]:
    """
    URLからコンテスト問題を取得する

    Parameters
    ----------

    url : str
        取得したいコンテストのURL

    Returns
    -------
    res: dict[str,str]
        問題URLの末尾とそのURLの辞書
    """

    contest = contest_from_url(url)

    contest_list = onlinejudge_run(contest, is_full=False, session='')
    res = {}
    for problem in contest_list["problems"]:
        res[problem["url"].split("/")[-1]] = problem["url"]
    return res
