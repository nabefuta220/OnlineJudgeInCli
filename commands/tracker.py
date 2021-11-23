"""
提出結果を解析する
"""
import argparse
import re
import time
from logging import getLogger

import bs4

from commands import CONFIG_FILE, LOGIN_URL
from commands.get_problem import get_html, login

logger = getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_track = subparser.add_parser('tracker')
    parser_track.add_argument('url')
    parser_track.add_argument('--config_file', default=CONFIG_FILE)


def parse(file):
    """
    提出結果と得点を解析する
    """
    submitte_state = {}
    target=r'<tr>\n<th .*>Submission Time</th>\n<td class="text-center"><time .*</time></td>\n</tr>'
    try:
        with open(file, 'r',encoding='UTF-8')as file_obj:
            soup = bs4.BeautifulSoup(file_obj, "html.parser")
        matchobj = re.search(
            r'<tr>\n<th>Score</th>\n<td .*/td>\n</tr>', str(soup.html))
        if matchobj:
            submitte_state["score"] = matchobj.group()
            matchobj = re.search(
                target, str(soup.html))
        if matchobj:
            submitte_state["time"] = matchobj.group()
        chose = soup.select('#judge-status')
        submitte_state["state"] = chose[0].text
    except TypeError as error:
        logger.error(error)
        return None

    return submitte_state





def track(url, config_file, output_file):
    """
    提出結果を解析する
    """
    session = login(LOGIN_URL+url, config_file)
    res = {}

    for _ in range(1, 300):
        get_html(url, output_file, session, True)
        res = parse(output_file)
        state = ""

        matchobj = re.search(r'[A-Z]+', res["state"])
        if matchobj:
            state = matchobj.group()

        if  state  not in ["WJ", "WR", ""]:
            logger.info("done!")
            matchobj2 = re.search(r'\d+', res["score"])
            matchobj3 = re.search(
                r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{4}', res["time"])
            res['time'] = matchobj3.group()
            res['score'] = matchobj2.group()
            res['state'] = state
            res['url'] = url

            return res
        logger.info("proceeding ... ( %s)",res['state'])
        time.sleep(1)
    logger.info("terminate due to long time taken")
    return None
