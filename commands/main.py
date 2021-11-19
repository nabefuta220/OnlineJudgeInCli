import argparse
import os

from commands import THIS_MODULE

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument('file')

    parse=arg.parse_args()

    read_file=parse.file

    print(read_file)
    with open(read_file,'r') as f:
        print(f.readlines()[:4])
    print("-----------")
    print(f"{THIS_MODULE}/../config.json")
    with open(f"{THIS_MODULE}/../config.json",'r') as f:
        print(f.readlines()[:4])