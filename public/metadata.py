#!/usr/bin/env python

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   metadata.py
@Time    :   2023/08/02 23:05:29
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''



#####################################################################################################
###*******************************************************************************************#######
###*************************                接口注释              *****************************#######
###*******************************************************************************************#######

class Tags(object) :
    def tags_metadata():
        tags_metadata = [
            {
                "name":"check",
                "description": "API接口检查",
            },
            # {
            #     "name":"APIS",
            #     "description": "开放的接口",
            # },
            # {
            #     "name": "users",
            #     "description": "认证后获取账户信息",
            # },
            # {
            #     "name": "get_token",
            #     "description": "获取海康token",
            # },
            # {
            #     "name": "accesstoken",
            #     "description": "自定义 Appkey/AppSecret token",
            # },
        ]
        return tags_metadata
    
