import re
from logger import logger

def get_data():
    str = ""
    while (True):
        try:
            s = input()
        except EOFError as e:
            return str
        else:
            str += s + " "
    return str


def get_submittion_URL(str):
    #logger.debug(str)
    matchobj = re.search(
        r'result: \S+', str)
    logger.debug(matchobj.group())
    terget = matchobj.group()[8:]
    #print("terget url= " + terget)
    return terget


if __name__ == "__main__":
    terget = get_submittion_URL(get_data())
    print("terget url= " + terget)
