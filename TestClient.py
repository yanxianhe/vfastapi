#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pytest, os, sys
sys.path.insert(0, os.path.abspath("."))

from fastapi.testclient import TestClient
from .main import app
from modules.module_route import Route

# 使用 TestClient 封装我们的 FastAPI 应用
client = TestClient(app)

# Mock 对象，用于模拟 Route.query() 方法的返回值
class MockRoute:
    @staticmethod
    def query():
        return [
            {
                "name": "探针",
                "method": "GET",
                "transaction_id": "ZR00001",
                "tags": "check",
                "description": "测试系统探针",
                "controller": "auth_controllers_ping",
                "path": "/api/ping",
                "system_id": "ZR0001",
                "transaction_status": "00",
                "created_at": "2024-04-08T13:39:48"
            }
        ]

# Mock 替换实际的 Route 模块的 query 方法
@pytest.fixture(autouse=True)
def mock_route_query(monkeypatch):
    monkeypatch.setattr(Route, "query", MockRoute.query)

# 测试 get_routes 函数
def test_get_routes():
    # 构建请求头和请求体
    headers = {
        "Secret-Key": "eyJzY29wZSI6WyJz",
        "Access-Key": "23977799",
    }
    data = {
        "type": "AK/SK",
        "pass_work": "False"
    }
    # 发送请求
    response = client.post("/routes", json=data, headers=headers)
    # 验证响应码和响应内容
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "探针",
            "method": "GET",
            "transaction_id": "ZR00001",
            "tags": "check",
            "description": "测试系统探针",
            "controller": "auth_controllers_ping",
            "path": "/api/ping",
            "system_id": "ZR0001",
            "transaction_status": "00", "created_at":"2024-04-08T13:39:48"
        }
    ]

def test_hello_world():
    # 构建请求头和请求体
    headers = {
        "Secret-Key": "eyJzY29wZSI6WyJz",
        "Access-Key": "23977799",
    }
    response = client.get("/hello", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message":{"_url":"http://testserver/hello"}} 

def test_ping():
    # 构建请求头和请求体
    headers = {
        "Secret-Key": "eyJzY29wZSI6WyJz",
        "Access-Key": "23977799",
    }
    response = client.get("/ping", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message":{"_url":"http://testserver/ping"}} 
if __name__ == "__main__":
    pytest.main()