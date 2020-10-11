# -*- coding: utf-8 -*-
"""
本模块提供一个公用的Logger，用于模块
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from coralquant.settings import CQ_Config as cfg


class Logger:
    """自定义日志记录类，默认把日志输出到文件和控制台 """

    def __init__(self,logger_name):

        log_path = cfg.LOG_PATH
        log_level = logging.INFO

        if cfg.IDB_DEBUG == '1':
            log_level = logging.DEBUG
            
        self.logger = logging.Logger(logger_name)
        self.logger.setLevel(log_level)
        
        # 定义一个按时间：天切分，保留15天的文件日志Handler
        fh = TimedRotatingFileHandler(
            log_path,
            when="D",  # 按天进行切分
            interval=1,  # 每天都切分
            backupCount=15,  # 保留15天的日志
            encoding="utf-8",  # 使用UTF-8的编码来写日志
            delay=False,
            utc=False,
        )  # (log_name,encoding='utf-8')
        fh.setLevel(log_level)

        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        formatter = logging.Formatter(
            "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        """获取记录器对象"""
        return self.logger




def main():
    log= Logger(__name__)

if __name__ == "__main__":
    main()
