
from onlinejudge_api.get_contest import main as onlinejudge_run
from .logger import logger
import onlinejudge.dispatch as dispatch


def generate(url: str) -> dict[str, str]:
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

    contest = dispatch.contest_from_url(url)

    str = onlinejudge_run(contest, is_full=False, session='')
    res = {}
    for i in str["problems"]:
        res[i["url"].split("/")[-1]] = i["url"]
    return res
