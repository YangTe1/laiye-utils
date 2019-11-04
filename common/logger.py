import logging
from logging.handlers import TimedRotatingFileHandler

from conf.config import log_level, normal_log_path, warn_log_path, error_log_path

"""
自建日志
"""

# 日志格式管理
formatter = logging.Formatter(
    '%(asctime)s %(process)d %(thread)d %(levelname)s %(message)s')
error_formatter = logging.Formatter((
    '%(asctime)s %(process)d '
    '%(thread)d %(pathname)s '
    '%(levelname)s %(message)s'
))

logger = logging.getLogger('nike_logger')
logger.setLevel(log_level)

###############################################################################
# 一般日志存放地址
loghd_info = logging.FileHandler(normal_log_path, encoding='utf-8')
loghd_info.setFormatter(formatter)
loghd_info.setLevel(log_level)

# 一周一个文件
# filehandler = TimedRotatingFileHandler(when='midnight', interval=7, filename=normal_log_path)
# filehandler.setFormatter(formatter)


# 警告日志，但文件存放，考虑到，应用存在优化空间，单独存放warn提供优化思路和提前预知隐患bug
logger_single_warn = logging.getLogger("logger_single_warn")
logger_single_warn.setLevel(logging.WARN)
loghd_single_warn = logging.FileHandler(warn_log_path, encoding='utf-8')
loghd_single_warn.setFormatter(formatter)
loghd_single_warn.setLevel(logging.WARN)

# 错误级别以上的日志单独存放，方便查找问题
loghd_error = logging.FileHandler(error_log_path, encoding='utf-8')
loghd_error.setFormatter(error_formatter)
loghd_error.setLevel(logging.ERROR)

# handler管理
logger.addHandler(loghd_info)
# logger.addHandler(filehandler)
logger.addHandler(loghd_single_warn)
logger.addHandler(loghd_error)
