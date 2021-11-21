import argparse
from commands import CONFIG_FILE
from .import creat


from .logger import logger

def add_subparser(subparser:argparse.Action) -> None:
    """
    ここのサブコマンド用引数を追加する
    """
    parser_get_contest=subparser.add_parser('generate')
    parser_get_contest.add_argument('file')
    parser_get_contest.add_argument('contest_name')

def generate(problems:dict[str,str],contest_name:str):
	"""
	コンテスト名と問題名、URLを読み込み、コンテスト名のディレクトリに回答用環境をいれる
	"""
	
	for folder, url in problems.items():
			#creat.creat(folder, url, load_file)
			creat.creat(f"{contest_name}/{folder}", url, CONFIG_FILE)
if __name__ == '__main__':
	generate('config.json')