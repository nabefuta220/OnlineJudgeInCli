"""
テスト用ファイル
"""
import argparse


from commands import THIS_MODULE


def main():
    """
    テスト用
    """
    arg=argparse.ArgumentParser()
    arg.add_argument('file')

    parse=arg.parse_args()

    read_file=parse.file

    print(read_file)
    with open(read_file,'r',encoding='UTF-8') as file:
        print(file.readlines()[:4])
    print("-----------")
    print(f"{THIS_MODULE}/../config.json")
    with open(f"{THIS_MODULE}/../config.json",'r',encoding='UTF-8') as file:
        print(file.readlines()[:4])
