"""
提出結果を解析する
"""
import argparse
import re
import time
from logging import getLogger

import bs4
from requests.sessions import Session

from commands import CONFIG_FILE
from commands.get_problem import get_html

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


def parse(file:str):
    """
    提出結果と得点を解析する

    Parameters
    ----------
    file : str
        提出情報ファイルのパス

    Returns
    -------
    submitte_state : Dict[str,any]
        提出情報: {"score":得点、"time":提出時間,"state":提出結果}
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





def track(url:str, output_file:str,session:Session):
    """
    提出結果を解析する

    Parameters
    ----------
    url : str
        提出結果のURL
    output_file : str
        提出情報の保存するファイルのパス
    session : request.session.Session
        ログイン情報

    Returns
    -------
    res : Dict[str,Any] | None
        提出結果の情報:{"state":提出結果、"score":得点、"time":提出日時、"url":提出URL}
    """
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
