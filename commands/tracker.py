"""
提出結果を解析する
"""
import argparse
from pathlib import Path
import re
import time
from logging import getLogger
from urllib.request import Request

import bs4

from commands import CONFIG_FILE, LOGIN_URL
from commands.get_problem import get_html
from commands.login import login

logger = getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_track = subparser.add_parser(
        'tracker', help='track sumission sesult')
    parser_track.add_argument('url', type=Path, help='track URL')
    parser_track.add_argument(
        '--config_file', type=Path, default=CONFIG_FILE, help='config file')


def parse(file: Path):
    """
    提出結果と得点を解析する

    Parameters
    ----------
    file : Path
        提出情報ファイルのパス

    Returns
    -------
    submitte_state : Dict[str,any]
        提出情報: {"score":得点、"time":提出時間,"state":提出結果}
    """
    submitte_state = {}
    filt = r'<tr>\n<th .*>Submission Time</th>\n<td class="text-center"><time .*</time></td>\n</tr>'
    try:
        with open(file, 'r', encoding='UTF-8')as file_obj:
            soup = bs4.BeautifulSoup(file_obj, "html.parser")
        matchobj = re.search(
            r'<tr>\n<th>Score</th>\n<td .*/td>\n</tr>', str(soup.html))
        if matchobj:
            submitte_state["score"] = matchobj.group()
            matchobj = re.search(
                filt, str(soup.html))
        if matchobj:
            submitte_state["time"] = matchobj.group()
        chose = soup.select('#judge-status')
        submitte_state["state"] = chose[0].text
    except TypeError as error:
        logger.error(error)
        return None

    return submitte_state


def track(url:str, output_file: Path, config_file: Path = CONFIG_FILE):
    """
    提出結果を解析する

    Parameters
    ----------
    url : str
        提出結果のURL
    output_file : Path
        提出情報の保存するファイルのパス
    config_file : Path (default = CONFIG_FILE)
        ユーザ情報が乗ったJSONファイルのパス

    Returns
    -------
    res : Dict[str,Any] | None
        提出結果の情報:{"state":提出結果、"score":得点、"time":提出日時、"url":提出URL}
    """
    res = {}
    session = login(url=f"{LOGIN_URL}{url}", config_file=config_file)
    for _ in range(1, 300):
        get_html(url=url, file=output_file,
                 session=session, force_rewrite=True)
        res = parse(output_file)
        state = ""

        matchobj = re.search(r'[A-Z]+', res["state"])
        if matchobj:
            state = matchobj.group()

        if state not in ["WJ", "WR", ""]:
            logger.info("done!")
            matchobj2 = re.search(r'\d+', res["score"])
            matchobj3 = re.search(
                r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{4}', res["time"])
            res['time'] = matchobj3.group()
            res['score'] = matchobj2.group()
            res['state'] = state
            res['url'] = url

            return res
        logger.info("proceeding ... ( %s)", res['state'])
        time.sleep(1)
    logger.info("terminate due to long time taken")
    return None
