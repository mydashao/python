import logging
import datetime
import sys

def log():
    # logger = logging.getLogger('mylogger')
    # logger.setLevel(logging.INFO)
    # stderr_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
    # stderr_handler.setLevel(logging.DEBUG)
    #
    # format = logging.Formatter(datefmt="%Y-%m-%d %H:%M:%S ",fmt="%(asctime)s - %(name)s - %(message)s")
    #
    # # rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    # stderr_handler.setFormatter(format)
    #
    # file_handler = logging.FileHandler('error.log')
    # file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(logging.Formatter(datefmt="%Y-%m-%d %H:%M:%S ",fmt="%(asctime)s - %(name)s - %(message)s"))
    # file_handler.setFormatter(logging)
    # logger.addHandler(stderr_handler)
    # logger.addHandler(file_handler)
    # return logger




    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.INFO)
    # 将日志消息发送到输出到Stream，如std.out, std.err或任何file-like对象。
    rf_handler = logging.StreamHandler(sys.stderr)
    # 设置handler将会处理的日志消息的最低严重级别
    rf_handler.setLevel(logging.DEBUG)
    # 设置消息格式，日期格式等
    format = logging.Formatter(fmt="%(asctime)s - %(name)s - %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    rf_handler.setFormatter(format)

    # 将日志消息发送到磁盘文件，默认情况下文件大小会无限增长
    f_handler = logging.FileHandler('error.log')
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(format)

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    return logger


def main():
    logger = log()
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    for i in range(10):
        logger.info(i)


main()