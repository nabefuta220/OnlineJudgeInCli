"""
問題文を整形する
"""
# pylint: disable=R0915
import os
import re
import sys
from logging import getLogger

import bs4
import requests
from requests.sessions import Session


logger = getLogger(__name__)


def get_html(url: str, file: str, session: Session, force_rewrite: bool = False):
    """
    問題URLを取得して保存する

    Parameters
    ----------
    url : str
        問題URL
    file:str
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


def parse(infile: str, outfile: str):
    """
    問題文にある表現をmarkdown用に変換する

    Parameters
    ----------
    infile : str
        変換したいファイルのパス
    outfile : str
        変換先のファイルのパス
    """
    try:
        with open(infile, 'r', encoding='UTF-8') as file:
            soup = bs4.BeautifulSoup(file, "html.parser")
        chose = soup.select('.lang-ja')
        if  not chose :
            logger.error("class leng-ja not found")
            chose = soup.select('#task-statement')
            if not chose :
                logger.error("id task-statement not found")
                sys.exit(1)
        string = ""
        try:
            string = "# " + soup.title.text + "\n\n"
        except AttributeError:
            logger.error("tag<title> not found")
        try:
            string += re.search(r'Time Limit: \d+ sec / Memory Limit: \d+ MB',
                                str(soup)).group()
        except AttributeError:
            logger.info("Time Limit and Memory Limit not found")

        #string += "\n\n" + re.sub(r'\n(\s)+', '', str(chose[0]))
        string += "\n\n"+str(chose[0])
        # string = re.sub(r'\n(\s)*', '', string)
        string = re.sub(r'<var>(\s|)*', '$', string)
        # string=string.replace("<var>",'$',-1)
        string = re.sub(r"(\s|)</var>", '$', string)
        string = string.replace("</font>", '</font>\n ', -1)
        string = string.replace(
            "<h3>", '### ', -1).replace("</h3>", '\n\n', -1)
        string = string.replace("</div>", '\n\n', -1)
        string = re.sub(r'<span class=".*">', '\n\n', string)
        string = string.replace("</span>", '', -1)
        string = re.sub(r'<div class=".*">', '\n\n', string)
        string = string.replace("<p>", '', -1)
        string = string.replace("</p>", '\n\n', -1)
        string = string.replace("<section>", '', -1)
        string = string.replace("</section>", '\n\n', -1)
        string = re.sub(r'<li>(\s|)+', '<li>', string)
        string = string.replace("<ol>", '', -1)
        string = string.replace("<ul>", '', -1)
        string = string.replace("</ol>", '\n', -1)
        string = string.replace("</ul>", '\n', -1)
        string = string.replace("<li>", '- ', -1)
        string = re.sub(r"(~\n)</li>", '$1\n', string)
        string = string.replace("</li>", '', -1)
        string = string.replace(
            "<strong>", '**', -1)
        string = string.replace("</strong>", '**', -1)
        string = string.replace("<hr/>", '----', -1)
        string = string.replace("<br/>", '', -1)
        string = string.replace("<code>", '`', -1)
        string = string.replace("</code>", '`', -1)
        string = re.sub(r'\n\n+', '\n\n', string)
        string = re.sub(r'<pre class=".*">', '<pre>', string)
        string = string.replace("\n</pre>", '</pre>', -1)
        string = string.replace("</pre>", '\n```', -1)
        string = string.replace("<pre>", '```text\n', -1)
        # string = re.sub(r'```text([^\s])', '```text\n $1', string)
        # string = string.replace('```text[^\n]', '```text\n', -1)
        string = string.replace("&lt;", '<', -1)
        string = string.replace("&gt;", '>', -1)
        try:
            with open(outfile, 'w', encoding='UTF-8') as file:
                file.write(string)
                logger.info("downloded problem as %s", outfile)
        except IsADirectoryError:
            logger.error('file %s is not file ...', outfile)
    except FileExistsError as error:
        logger.error(error)


def get_problem(url: str, file: str, session: Session):
    """
    ログインして、問題文を取得する

    Parameters
    ----------
    url : str
        問題URL
    file : str
        保存先のファイルのパス
    session : requests.session.Session
        ログイン情報
    """

    save_url = f"{file}_tmp.html"
    get_html(url, save_url, session)
    parse(save_url, file)
