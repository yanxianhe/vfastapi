import requests
from xml.etree import ElementTree as ET
 
# 定义API地址和登录认证信息
url = "http://192.168.4.1/api/getSysInfo"
username = "admin"
password = "716716716"
 
# 构建XML请求体
xml_request = '''<?xml version="1.0"?>
                    <sys-info>
                        <sn></sn>
                    </sys-info>'''
headers = {'Content-Type': 'application/xml'}
auth = (username, password)
 
try:
    # 发送POST请求并接收返回结果
    response = requests.post(url, data=ET.tostring(ET.fromstring(xml_request)), headers=headers, auth=auth)
    
    if response.status_code == 200:
        # 提取SN值
        root = ET.fromstring(response.text)
        sn = root[0].text
        
        print("SN:", sn)
    else:
        print("Failed to retrieve SN",response.status_code)
except Exception as e:
    print("Error occurred:", str(e))