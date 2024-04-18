#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2023/08/07 21:29:00
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''

import asyncio
import importlib
import os
import threading
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests,urllib3,json,logging

import logging
from datetime import datetime, timedelta
from typing import Union
from fastapi import Body, FastAPI, Header, Request
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger

from public.schedule_job import ScheduleJob
### ssl 
urllib3.disable_warnings()
logging.captureWarnings(True)
description = """"""

# #################################################*#################################################
###*******************************************************************************************#######
###*************************           controllers init          *****************************#######
###*********************************  初始化 controllers  *************************************#######
###*******************************************************************************************#######

# from internal.auth.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from public.metadata import Tags
from modules.module_route import Route

## controllers
from controllers import auth_controllers
# 将controllers文件的函数注册到当前全局命名空间中，全局中函数名字不能重复，建议使用模块名+函数名
# globals()[auth_controllers.auth_controllers_get_token.__name__] = auth_controllers.auth_controllers_get_token
globals()[auth_controllers.auth_controllers_ping.__name__] = auth_controllers.auth_controllers_ping
## 也可使用循环注册 不推荐
# 导入整个模块之后，使用 dir() 函数获取模块中的所有对象
# module_objects = dir(auth_controllers)
# # 遍历模块中的对象列表
# for obj_name in module_objects:
#     # 检查对象是否为函数
#     if callable(getattr(auth_controllers, obj_name)):
#         # 将函数添加到当前全局命名空间中
#         globals()[obj_name] = getattr(auth_controllers, obj_name)



#####################################################################################################
###*******************************************************************************************#######
###*************************             FastAPI init            *****************************#######
###*******************************************************************************************#######
try:
    tags_metadata = Tags.tags_metadata()
    app = FastAPI(
        title="openAPI",
        description=description,
        summary="",
        version="v0.0.1",
        # docs_url=None,
        redoc_url=None,
        openapi_tags=tags_metadata,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 将静态文件目录配置为 static 文件夹
    app.mount("/static", StaticFiles(directory="static"), name="static")
    # # 设置Jinja2模板目录
    templates = Jinja2Templates(directory="static")
    logger.success("[success] running  http://0.0.0.0:8000 (Press CTRL+C to quit) ")
except Exception as e:
    logger.error("[error] running  %s" % e)
    raise e


#####################################################################################################
###*******************************************************************************************#######
###*************************           API v 1.0 routes          *****************************#######
###*******************************************************************************************#######


# API 示例处理函数 例子官方默认
@app.get("/hello",tags=["check"], include_in_schema=False)
async def hello_world(request: Request):
    logger.debug(request.url)
    return {"message": request.url}


# API 示例处理函数 异步路由把controllers单独放到指定目录下 auth_controllers.auth_controllers_ping
@app.get("/ping",tags=["check"], include_in_schema=False)
async def ping(request: Request):
    return await auth_controllers.auth_controllers_ping(request)


## 查询路由
@app.post("/routes",tags=["APIS"], include_in_schema=False)
async def get_routes(
    request: Request,
    secret_key: str = Header("eyJzY29wZSI6WyJz", description="Secret Key"),
    access_key: str = Header("23977799", description="Access Key"),
    type: str = Body("AK/SK",embedy=True),
    pass_work: bool = Body("False",embedy=True)):
    _routes = Route.query()
    logger.debug(_routes)
    return _routes


###********************** 路由例子 通过数据接口表维护接口 interfaces **********************#######
# 目的：通过接口表维护接口简化mian.py文件及controllers分离。增加接口维护
# 应用程序启动时注册路由
@app.on_event("startup")
async def startup_event():
    # 加载路由
    if os.environ.get('LOAD_ROUTING', 'true') == 'true' :
        logger.info("loading routes ::::::::::::::::::")
        register_routes()
    else :
        logger.warning("not loading routes ::::::::::::::")

    # 启动一个协程 MainThread
    # asyncio.create_task() 用于并发地执行单个协程，并将其封装成一个可管理的任务
    asyncio.create_task(ScheduleJob.sys_warning_job())
    # 启动一个线程
    ScheduleJob.schedule_sys_warning()
    
# API 注册路由,将controllers文件的函数注册到当前全局命名空间中，全局中函数名字不能重复，建议使用模块名+函数名
def register_routes():
    _routes = Route.query()
    for route in _routes:
        method = getattr(app, route.method.lower())
        controller = globals().get(route.controller)
        if method and controller:
            method(route.path,tags=[route.tags],description=route.description)(controller)
            #method(route.path,tags=[route.tags],description=route.description,include_in_schema=False)(controller)





#####################################################################################################
###*******************************************************************************************#######
###*************************           UI v 1.0 routes           *****************************#######
###*******************************************************************************************#######

# 主页面
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
    # 渲染/static/pages/index.html模板
    return templates.TemplateResponse("pages/index.html", {"request": request})

# 登录页面
@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def read_login(request: Request):
    # 渲染/static/pages/index.html模板
    return templates.TemplateResponse("pages/index.html", {"request": request})



# auth.read_token
# async def read_token(
#     request: Request,
#     service_addres: str = Header("https://172.16.0.17", description="https://ip:port"),
#     access_key: str = Header("23977799", description="Access Key")):
    
#     # secret_key = _autn.get(access_key)
#     # if not secret_key:
#     #     return "msg:无此账号 %s" % access_key
    
#     # _uuid = getUuid1()
#     # _requrl = ("%s%s")%(service_addres,_ARTEMIS_TOKEN)
#     # logging.info(("[%s][%s] {%s} " % (_uuid,request.client.host ,_requrl)))
#     #  ## 获取存储在Redis中的JSON数据
#     # _token_json = get_token(access_key)
#     # if _token_json is not None:
#     #     access_token = json.loads(_token_json)
#     #     logging.info(("[%s] {%s}" % (_uuid, access_token)))
#     #     return access_token
#     # ## 通过接口获取
#     # _xcasignature,_headers = getSignature(access_key,secret_key,_ARTEMIS_TOKEN);
#     # access_token = send_http(_uuid,_requrl,_headers)
#     # # 设置键-值对，将JSON存储到Redis中，并设置过期时间为11小时
#     # pull_token(access_key,json.dumps(access_token))
#     # logging.info(("[%s] {%s}" % (_uuid, access_token)))

#     return "access_token"

# # ak = "23977799"
# # sk = 'onihBfjbZfkgUNnsnKbD'
# # url = "/artemis/api/v1/oauth/token"
# @app.get("/v1/token",tags=["token"])
# async def read_token(ak: str,sk: str,requrl:str, request: Request):
#     _uuid = UtilsTools().getUuid1()
#     logging.info(("[%s][%s] {%s} " % (_uuid,request.client.host ,request.url)))

#     char = requrl.find("/artemis/")
#     req_url1 = requrl[char:]
    
#     payload = {}
#     ## 海康获取 x-ca-signature 返回headers
#     headers = hmacsha_toos.xcasignature(ak,sk,req_url1)

#     try:
#         response = requests.request("POST", requrl, headers=headers, data=payload,verify=False,timeout=15)
#         data = (json.loads(response.text))
#         if data["msg"] == "success" :
#             access_token = data["data"]
#         else:
#             access_token == data
#     except requests.exceptions.Timeout :
#         return {"error":"Internal Server TimeoutException"}
#     except requests.exceptions.ConnectionError:
#         return {"error":"Internal Server Exception"}
    
#     logger.info("[%s] {%s}" % (_uuid, access_token))
#     return access_token


# #####################################################################################################

# ## 自定义 AccessCode
# @app.post("/v1.1/token",tags=["accesstoken"])
# async def read_token(request: Request):
#     client_host = request.client.host
#     flg = True
#     for Appkey in request.headers.keys():
#         if Appkey.find("zr_")!= -1:
#             AppSecret = request.headers.get(Appkey)
#             msg = ("%s:%s") % (Appkey,AppSecret)
#             logger.info("[%s] {%s}" % (client_host, msg))
#             flg = False
#         else :
#             pass
#     if flg :
#         return {"error":"Internal Server Exception"}
#     else:
#         pass
#         logger.info("[%s] {%s}" % (client_host, request.headers))
#         data = {"access_token":client_host}
#         return data
