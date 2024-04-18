#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   module_route.py
@Time    :   2023/08/07 23:36:27
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''



import pymysql
from sqlalchemy import TIMESTAMP, Column, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modules.db_client import MySQLAlchemyClient
from loguru import logger
from public.get_logging import GetLogging


# 引入日志
GetLogging().get()
# 以便与 SQLAlchemy 兼容 ORM
pymysql.install_as_MySQLdb()
# 声明基类
Base = declarative_base()


class Route(Base):
    __tablename__ = "interfaces"
    __table_args__ = {"comment": "主路由接口表."}
    transaction_id = Column(String(32), primary_key=True, comment="接口交易码id")
    name = Column(String(254), nullable=False, comment="接口名")
    path = Column(String(254), nullable=False, comment="接口路径")
    method = Column(String(16), nullable=False, comment="请求方式")
    controller = Column(String(254),nullable=False,server_default="hello_world",comment="接口controller入口",)
    system_id = Column(String(16), nullable=False, comment="系统id")
    tags = Column(String(64), nullable=False, comment="接口tags描述在metadata维护")
    transaction_status = Column(String(16), nullable=False, server_default="00", comment="接口状态 00:正常 01:测试接口 02:停止对外服务")
    description = Column(String(254), nullable=False, comment="接口描述信息")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    def __init__(self,transaction_id,name,path,method,controller,system_id,tags,transaction_status,description,created_at):
        self.transaction_id = transaction_id
        self.name = name
        self.path = path
        self.method = method
        self.controller = controller
        self.system_id = system_id
        self.tags = tags
        self.transaction_status = transaction_status
        self.description = description
        self.created_at = created_at


    ## toString
    def __str__(self):
        _interfaces = f"(transaction_id={self.transaction_id},name={self.name},path={self.path},method={self.method},controller={self.controller},system_id={self.system_id},tags={self.tags},transaction_status={self.transaction_status},description={self.description},created_at={self.created_at})"
        return _interfaces


    def query():
        _results = ""
        _myquery = MySQLAlchemyClient()
        _MySession = sessionmaker(bind=_myquery.engine)
        try:
            _session = _MySession()
            _query = _session.query(Route)
            logger.debug("query SQL:\t{%s} " % _query)
            _results = _query.all()
        except Exception as e:
            logger.error("error:\t{%s}" % e)
            return e
        finally :
            _session.close()
        return _results
    
try:
    ## 创建会话
    _my = MySQLAlchemyClient()
    Session = sessionmaker(bind=_my.engine)
    ## 创建表如果存在 ，则忽略
    Base.metadata.create_all(_my.engine)
except Exception as e:
    logger.error("Route.query  error ,%s " % e)

class StaticPage(Base):
    __tablename__ = 'static_page'
    __table_args__ = {"comment": "前端页面路由."}

    transaction_id = Column(String(32), primary_key=True, comment='页面交易码id')
    name = Column(String(255), nullable=False, comment='页面名')
    path = Column(String(255), nullable=False, comment='路径')
    method = Column(String(16), default="GET", comment='请求方式')
    system_id = Column(String(16), nullable=False, comment='系统id')
    transaction_status = Column(String(64), nullable=False, default='00', comment='页面状态 00:正常 01:测试接口 02:停止对外服务')
    description = Column(String(255), nullable=False, comment='功能描述')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')

    def __init__(self, transaction_id, name, path, method="GET", system_id=None, transaction_status="00", description=None):
        self.transaction_id = transaction_id
        self.name = name
        self.path = path
        self.method = method
        self.system_id = system_id
        self.transaction_status = transaction_status
        self.description = description

    def __str__(self):
        return f"StaticPage(transaction_id='{self.transaction_id}', name='{self.name}', path='{self.path}', method='{self.method}', system_id='{self.system_id}', transaction_status='{self.transaction_status}', description='{self.description}', created_at='{self.created_at}')"
    
    def get_by_id(transaction_id):
        _results = ""
        _myquery = MySQLAlchemyClient()
        _MySession = sessionmaker(bind=_myquery.engine)
        try:
            _session = _MySession()
            _query = _session.query().filter_by(transaction_id=transaction_id).first()
            logger.debug("query SQL:\t{%s} " % _query)
            _results = _query.all()
        except Exception as e:
            logger.error("StaticPage.get_by_id:: \t{%s}" % e)
            return e
        finally :
            _session.close()
        return _results
    
    def get_paginated(page=1, per_page=20):
        _results = ""
        _myquery = MySQLAlchemyClient()
        _MySession = sessionmaker(bind=_myquery.engine)
        try:
            _session = _MySession()
            query = _session.query()
            total_count = query.count()
            pages = total_count // per_page + (1 if total_count % per_page > 0 else 0)
            pages = max(pages, 1)
            offset = (page - 1) * per_page
            _query = query.offset(offset).limit(per_page)
            logger.debug("query SQL:\t{%s} " % _query)
            results = _query.all()
        except Exception as e:
            logger.error("StaticPage.get_paginated:: \t{%s}" % e)
            return e
        finally :
            _session.close()
        return results, total_count, pages
    
    def create(static_page):
        _results = ""
        _myquery = MySQLAlchemyClient()
        _MySession = sessionmaker(bind=_myquery.engine)
        try:
            _session = _MySession()
            _session.add(static_page)
            _session.commit()
        except Exception as e:
            logger.error("StaticPage.create:: \t{%s}" % e)
            return e
        finally :
            _session.close()
        return _results


    def update(self, session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
try:
    ## 创建会话
    _my = MySQLAlchemyClient()
    Session = sessionmaker(bind=_my.engine)
    ## 创建表如果存在 ，则忽略
    Base.metadata.create_all(_my.engine)
except Exception as e:
    logger.error("Route.query  error ,%s " % e)
# session = Session()
# # 分页查询
# page_size = 20  # 每页的记录数
# page_number = 1  # 页码，从1开始

# # 计算偏移量
# offset = (page_number - 1) * page_size
# # 查询数据并进行分页
# results = session.query(Route).offset(offset).limit(page_size).all()


# json_list = []
# # 遍历结果
# for result in results:
#     # 处理每条记录
#     json_list.append(result)
#     print("%s"%result)
    

