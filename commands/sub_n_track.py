"""
提出URLを取得して、結果を監視する
"""
import argparse
import pathlib
import subprocess
from logging import getLogger

from onlinejudge.utils import default_cookie_path

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
    parser_sub_n_track = subparser.add_parser(
        'subntrack', help='submit your soultion and track your result')
    parser_sub_n_track.add_argument(
        'file', type=pathlib.Path, help='file to submit')


def submittd_n_track(file: str):
    """
    提出して、結果を見る

    Parameters
    ----------
    file : str
        提出するソースコードのパス
    """

    tmp_file = f"{THIS_MODULE}/../res.tmp"
    logger.info(tmp_file)
    args = argparse.Namespace(url=None, file=file, open=False, cookie=default_cookie_path,
                              language=None,   guess=True, guess_cxx_latest=True,
                              guess_cxx_compiler='gcc',  guess_python_version='auto',
                              guess_python_interpreter='cpython', wait=1, yes=True)
    print(args)

    command = f'oj s {file} --no-open -y'
    with open(file=tmp_file, encoding='UTF-8', mode="w") as out_tmp:
        subprocess.run(shell=True, args=command, check=True,
                       stdout=out_tmp, encoding='UTF-8')

    with open(tmp_file, 'r', encoding='UTF-8')as file_obj:
        res = file_obj.read()
        print(res)

    url = submittgetter.get_submittion_url(res)
    logger.info("submittion: %s", url)
    print(tracker.track(url=url,  output_file='tmp.html'))
