"""
ログ出力
"""
import logging


if __name__ == '__main__':
    logger = logging.getLogger('LoggingTest')

    # ログレベルの設定
    logger.setLevel(logging.DEBUG)

    # ログのコンソール出力の設定
    sh = logging.StreamHandler()
    logger.addHandler(sh)

    # ログの出力形式の設定
    formatter = logging.Formatter(
        '[%(levelname)s] %(message)s')

    sh.setFormatter(formatter)
