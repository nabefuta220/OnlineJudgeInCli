import logging
"""
class logger:

    def __init(self)__:
        pass
"""

if False :
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

    """

    logger.log(20, 'info')
    logger.log(30, 'warning')
    logger.log(100, 'test')

    logger.info('info')
    logger.warning('warning')
    """