"""
問題文を整形する
"""
# pylint: disable=R0915
import json
import os
import re
from logging import getLogger
import sys

import bs4
import requests
from requests.sessions import Session

from commands import LOGIN_URL

logger = getLogger(__name__)


def get_html(url:str, file:str, session:Session, force_rewrite:bool=False):
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
        logger.info("file: %s is already exist",file)
    else:
        try:
            with open(file, 'w',encoding='UTF-8') as write_file:
                source = session.get(url)
                source.raise_for_status()
                soup = bs4.BeautifulSoup(source.text, "html.parser")
                write_file.write(str(soup))
        except requests.exceptions.HTTPError as error:
            logger.error(error)
            os.remove(file)
            sys.exit(error)
        logger.debug("saved %s as %s",url,file)


def parse(infile:str,outfile:str):
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
        with open(infile, 'r',encoding='UTF-8') as file:
            soup = bs4.BeautifulSoup(file, "html.parser")
        chose = soup.select('.lang-ja')
        if chose == []:
            logger.error("class leng-ja not found")
            chose = soup.select('#task-statement')
            if chose == []:
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

        string += "\n\n" + re.sub(r'\n(\s)+', '', str(chose[0]))
        # string = re.sub(r'\n(\s)*', '', string)
        string = re.sub(r'<var>(\s|)*', '$', string)
        # string=string.replace("<var>",'$',-1)
        string = re.sub(r"(\s|)</var>", '$', string)
        string = string.replace("</font>", '</font>\n ', -1)
        string = string.replace("<h3>", '### ', -1).replace("</h3>", '\n\n', -1)
        string = string.replace("</div>", '\n\n', -1)
        string = re.sub(r'<span class=".*">', '\n\n', string)
        string = string.replace("</span>", '', -1)
        string = re.sub(r'<div class=".*">', '\n\n', string)
        string = string.replace("<p>", '', -1).replace("</p>", '\n\n', -1)
        string = string.replace("<section>", '', -1).replace("</section>", '\n\n', -1)
        string = re.sub(r'<li>(\s|)+', '<li>', string)
        string = string.replace("<ol>", '', -1).replace("</ol>", '\n', -1)
        string = string.replace("<ul>", '', -1).replace("</ul>", '\n', -1)
        string = string.replace("<li>", '- ', -1)
        string = re.sub(r"(~\n)</li>", '$1\n', string).replace("</li>", '', -1)
        string = string.replace("<strong>", '**', -1).replace("</strong>", '**', -1)
        string = string.replace("<hr/>", '----', -1).replace("<br/>", '', -1)
        string = string.replace("<code>", '`', -1).replace("</code>", '`', -1)
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
            with open(outfile, 'w',encoding='UTF-8') as file:
                file.write(string)
                logger.info("downloded problem as %s",outfile)
        except IsADirectoryError:
            logger.error('file %s is not file ...',outfile)
    except FileExistsError as error:
        logger.error(error)


def login(url:str, config_file:str):
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
    # print(url)
    res = session.get(url)
    # print(res.text)
    page = bs4.BeautifulSoup(res.text, 'lxml')
    csrf_token = page.find(attrs={'name': 'csrf_token'}).get('value')
    try:
        with open(config_file, 'r',encoding='UTF-8') as config:
            info = json.load(config)["user_info"]
        login_info = {
            "csrf_token": csrf_token,
            "username": info["username"],
            "password": info["password"],
        }
        session.post(url, data=login_info)
    except FileNotFoundError:
        logger.error("config file :%s not found",config_file)
    except KeyError:
        logger.error(
            "to login, key:user_info[username], user_info[password] needed in %s",config_file)
    return session


def get_problem(url:str, file:str, config_file:str):
    """
    ログインして、問題文を取得する

    Parameters
    ----------
    url : str
        問題URL
    file : str
        保存先のファイルのパス
    config_file : str
        ユーザー情報が乗ったファイルのパス
    """
    session = login(LOGIN_URL+url, config_file)

    get_html(url, file+'_tmp.html', session)
    parse(file+'_tmp.html', file)
