"""
提出URLを取得する
"""
import re
from logging import getLogger

logger = getLogger(__name__)


def get_data():
    """
    文字を標準入力から取得する

    Returns
    -------
    res : str
        読み取った文字列
    """
    res = ""
    while True:
        try:
            url = input()
        except EOFError:
            return res
        else:
            res += url + " "


def get_submittion_url(source:str):
    """
    標準入力から提出URLを抽出する

    Parameters
    ----------
    source : str
        提出情報の標準エラー出力

    Returns
    -------
    terget_url :str
        提出情報のURL
    """
    matchobj = re.search(
        r'result: \S+', source)
    logger.debug(matchobj.group())
    terget_url = matchobj.group()[8:]
    return terget_url


if __name__ == "__main__":
    terget = get_submittion_url(get_data())
    print("terget url= " + terget)
