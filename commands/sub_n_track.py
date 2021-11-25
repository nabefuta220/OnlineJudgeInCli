"""
提出URLを取得して、結果を監視する
"""
import argparse
import subprocess
from logging import getLogger


from commands import THIS_MODULE, submittgetter, tracker

logger = getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_sub_n_track = subparser.add_parser('subntrack')
    parser_sub_n_track.add_argument('file')




def submittd_n_track(file:str):
    """
    提出して、結果を見る

    Parameters
    ----------
    file : str
        提出するソースコードのパス
    cession: Requests.session.Session
        ログイン情報
    """

    tmp_file = f"{THIS_MODULE}/../res.tmp"
    with open(tmp_file, 'w',encoding='UTF-8'):
        pass
    command = f'oj s {file} --no-open -y >> {tmp_file}'
    subprocess.run(shell=True, args=command,check=True)
    with open(tmp_file, 'r',encoding='UTF-8')as file_obj:
        res = file_obj.read()
        print(res)

    url = submittgetter.get_submittion_url(res)
    logger.info("submittion: %s",url)
    print(tracker.track(url=url,  output_file='tmp.html'))
