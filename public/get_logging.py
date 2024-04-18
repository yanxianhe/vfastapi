#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sys_logs.py
@Time    :   2023/08/07 08:58:06
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''

import os , time
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEFAULT').upper()
LOG_FILENAMES = {
    'ERROR': "error_{time:YYYY-MM-DD}.log",
    'WARNING':"warning_{time:YYYY-MM-DD}.log",
    'INFO': "info_{time:YYYY-MM-DD}.log",
    'SUCCESS': "success_{time:YYYY-MM-DD}.log",
    'DEFAULT': "syslogs_{time:YYYY-MM-DD}.log"
}
log_filename = LOG_FILENAMES.get(LOG_LEVEL, LOG_FILENAMES['DEFAULT'])
log_path = os.path.join(BASE_DIR, "logs/" + log_filename)

class GetLogging:
    """
    日志配置 根据自己情况设置
    """
    def __init__(self):
        # 标识号
        if log_filename.split("_")[0] == "syslogs":
            # 默认日志文件,输出控制台
            logger.add(
                log_path,
                format="{time:YYYY-MM-DD HH:mm:ss} {level} {file}:{function} {line} --> {message}",
                rotation="00:00", retention=7, level='DEBUG', encoding='utf-8', 
                backtrace=True, diagnose=True,
            )
        else :
            logger.remove()
            logger.add(
                log_path,
                format="{time:YYYY-MM-DD HH:mm:ss} {level} {file}:{function} {line} --> {message}",
                # 关闭日志记录的过滤器
                # filter=lambda x: True if x["level"].name == LOG_LEVEL else False,
                rotation="00:00", retention=7, level=LOG_LEVEL, encoding='utf-8',
                backtrace=True, diagnose=True, 
            )
            
        self.logger = logger
 
    def get(self):
        return self.logger

# 假设日志文件存放在当前目录下的logs文件夹中
# 删除30天前的日志文件
class CleanLogging:
    @staticmethod
    def clean_logs():
        """删除30天前的日志文件"""
        logs_dir = os.path.join(BASE_DIR, "logs")
        current_time = time.time()
        cutoff_time = current_time - 30 * 24 * 60 * 60

        try:
            for filename in os.listdir(logs_dir):
                file_path = os.path.join(logs_dir, filename)
                if os.path.isfile(file_path):
                    file_modification_time = os.path.getmtime(file_path)
                    if file_modification_time < cutoff_time:
                        try:
                            print(f"Removed old log file: {filename}")
                            #os.remove(file_path)
                        except Exception as e:
                            print(f"Failed to remove {filename} due to: {e}")
        except Exception as e:
            print(f"An error occurred while cleaning logs: {e}")
# Usage example
if __name__ == '__main__':

    globalLog = GetLogging().get()
    logger.debug("[debug] 测试 debug 级别,记录 [debug] [info] [success] [error] 级别日志")
    logger.info("[info] 测试级别日志")
    logger.success("[success] 测试级别日志")
    logger.warning("[warning] 测试级别日志")
    logger.error("[error] 测试级别日志")
    pass