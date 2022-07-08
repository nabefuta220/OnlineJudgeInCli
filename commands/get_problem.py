"""
問題文を整形する
"""
# pylint: disable=R0915
import json
import os
import re
import sys
from logging import getLogger
from pathlib import Path
from urllib.request import Request
import bs4
import requests
from requests.sessions import Session


logger = getLogger(__name__)


def get_html(url: str, file: Path, session: Session, force_rewrite: bool = False):
    """
    問題URLを取得して保存する

    Parameters
    ----------
    url : str
        問題URL
    file: Path
        保存先のファイルパス
    session : requests.sessions.Session
        ログイン情報
    force_rewrite : bool (default = False)
        強制上書きを許可するか
    """
    if os.path.isfile(file) and not force_rewrite:
        logger.info("file: %s is already exist", file)
    else:
        try:
            with open(file, 'w', encoding='UTF-8') as write_file:
                source = session.get(url)
                source.raise_for_status()
                soup = bs4.BeautifulSoup(source.text, "html.parser")
                write_file.write(str(soup))
        except requests.exceptions.HTTPError as error:
            logger.error(error)
            os.remove(file)
            sys.exit(error)
        logger.debug("saved %s as %s", url, file)


def parse(infile: Path, outfile: Path, config_file: Path):
    """
    問題文にある表現をmarkdown用に変換する

    Parameters
    ----------
    infile : Path
        変換したいファイルのパス
    outfile : Path
        変換先のファイルのパス
    config_file : Path
        変換法則をまとめたJSONファイル
    """
    # 問題分のhtmlファイルから問題文部分を抽出する
    try:
        with open(infile, 'r', encoding='UTF-8') as file:
            soup = bs4.BeautifulSoup(file, "html.parser")
        chose = soup.select('.lang-ja')
        if not chose:
            logger.error("class leng-ja not found")
            chose = soup.select('#task-statement')
            if not chose:
                logger.error("id task-statement not found")
                sys.exit(1)
        #問題タイトルを抽出する
        try:
            string = f"# {soup.title.text}\n\n"
        except AttributeError:
            logger.error("tag<title> not found")
            string = ""
        #実行時間制限と実行メモリ制限を取得する
        try:
            string += re.search(r'Time Limit: \d+ sec / Memory Limit: \d+ MB',
                                str(soup)).group()
        except AttributeError:
            logger.info("Time Limit and Memory Limit not found")

        string += f"\n\n{chose[0]}"
        # ファイルから変換法則を読み込み、変換する
        try:
            with open(config_file, encoding='UTF-8', mode='r')as config:
                convert = json.load(config)["convert"]
                for search, replace in convert.items():
                    string = re.sub(search, replace, string)
        except FileNotFoundError:
            logger.error('configfile : %s not found', config_file)
        except KeyError:
            logger.error(
                "key: convert in config file: % s not found", config_file)
        #変換した問題分をファイルに書き込む
        try:
            with open(outfile, 'w', encoding='UTF-8') as file:
                file.write(string)
                logger.info("downloded problem as %s", outfile)
        except IsADirectoryError:
            logger.error('file %s is not file ...', outfile)
    except FileExistsError as error:
        logger.error(error)


def get_problem(url: Request, file: Path, config_file: Path, session: Session):
    """
    ログインして、問題文を取得する

    Parameters
    ----------
    url : urllib.request.Request
        問題URL
    file : Path
        保存先のファイルのパス
    config_file : Path
        変換法則をまとめたJSONファイル
    session : requests.session.Session
        ログイン情報
    """

    save_url = f"{file}_tmp.html"
    get_html(url, save_url, session)
    parse(save_url, file, config_file=config_file)
