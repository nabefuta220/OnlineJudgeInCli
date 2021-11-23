"""
提出URLを取得する
"""
import re
from logging import getLogger

logger = getLogger(__name__)


def get_data():
    """
    文字を標準入力から取得する
    """
    res = ""
    while True:
        try:
            url = input()
        except EOFError:
            return res
        else:
            res += url + " "
    return res


def get_submittion_url(source):
    """
    標準入力から提出URLを抽出する
    """
    matchobj = re.search(
        r'result: \S+', source)
    logger.debug(matchobj.group())
    terget_url = matchobj.group()[8:]
    return terget_url


if __name__ == "__main__":
    terget = get_submittion_url(get_data())
    print("terget url= " + terget)
