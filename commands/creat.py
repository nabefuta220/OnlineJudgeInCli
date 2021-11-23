"""
回答環境を構築する
"""
import argparse
import json
import os
import subprocess
from logging import getLogger

from commands import CONFIG_FILE
from commands.get_problem import get_problem



logger=getLogger(__name__)


def add_subparser(subparser: argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する

    Parameters
    ----------
    subparser : argparse.Action
            サブコマンドを格納するパーサー
    """
    parser_create = subparser.add_parser('creat')
    parser_create.add_argument('file')
    parser_create.add_argument('--config_file','-c', default=CONFIG_FILE)
    parser_create.add_argument('-u', '--url')


def creat(file, url,config_file):
    """
    問題回答環境を作成する
    """
    os.makedirs(file)
    try:
        with open(config_file,encoding='UTF-8' ,mode='r') as config:
            presets = json.load(config)["preset"]
            for file_name in presets.keys():
                open_file=f"{file}/{file_name}"
                with open(open_file, encoding='UTF-8',mode="w") as out_file:
                    for strings in presets[file_name]:
                        out_file.write(strings + "\n")
                logger.info("created %s/%s",file,file_name)

    except FileNotFoundError :
        logger.error('configfile : %s not found',config_file)

    if url :
        try:
            subprocess.run(command=f"cd {file} && oj d {url}", check=True, shell=True)
        except subprocess.CalledProcessError as ex:
            print(ex)
        else:
            creat_file=f"{file}/{url.split('/')[-1]}.md"
            get_problem(url, creat_file,config_file)
