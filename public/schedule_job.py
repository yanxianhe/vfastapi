#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :schedule_job.py
@doc         :
@Time        :2024/04/17 12:17:48
@Author      :yxh
@Version     :1.0
@Contact     :xianhe_yan@sina.com
'''

import threading
import asyncio , time
from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class ScheduleJob:
    def __init__():
        
        pass
    def job_print_thread_id():
        thread_id = threading.current_thread().ident
        thread_name = threading.current_thread().name
        return ("%s::%s"%(thread_name,thread_id))
    '''
    # 首次主程序启动是执行任务一次,然后间隔 N 小时执行一次
    # 间隔 N 小时执行一次,需要等待上次任务执行完成 [while True]
    # [问题是while循环中sleep会阻塞主线程,需要单独协程处理]
    # 定时任务启动单独的协程
    '''
    async def sys_warning_job():
        job_print_thread_id = ScheduleJob.job_print_thread_id()
        while True:
            logger.warning("%s :: The system initiates a coordinated heartbeat alarm "% job_print_thread_id)
            await asyncio.sleep(60 * 60 * 24) # 间隔 24 小时执行一次
    def sys_warning_task_job():
        job_print_thread_id = ScheduleJob.job_print_thread_id()
        while True:
            logger.warning("%s :: Heartbeat alert for system startup threads"% job_print_thread_id)
            time.sleep(60 * 2)
    def sys_warning_schedule():
        job_print_thread_id = ScheduleJob.job_print_thread_id()
        logger.warning("%s :: Heartbeat alert for system startup threads"% job_print_thread_id)
    
    '''
    # Cron 表达式,不考虑上次任务执行完成情况
    # 定时任务启动单独的协程
    '''
    def schedule_sys_warning():
        logger.debug("The system warning task init to start")
        scheduler = BackgroundScheduler()
        try:
            # Cron 表达式 分钟（0-59）小时（0-23）日期（1-31）月份（1-12）星期几（0-6，0 表示星期日）
            scheduler.add_job(ScheduleJob.sys_warning_schedule, CronTrigger.from_crontab("0 1 * * *")) # 每天凌晨1点执行一次
            scheduler.add_job(ScheduleJob.sys_warning_schedule, CronTrigger.from_crontab("0 0 1 * *")) # 每月1日凌晨0点执行一次
            scheduler.start()
        except Exception as e:
            logger.error("The system warning task failed to start")

def main():
    # asyncio.run() 用于运行整个异步应用程序的主事件循环
    # asyncio.run(ScheduleJob.sys_warning_job())
    ScheduleJob.schedule_sys_warning()
    input("防住主程序退出按下 Enter 键退出程序...\n")
if __name__ == "__main__":
    main()