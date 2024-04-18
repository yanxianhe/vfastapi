#### 指定项目使用python 版本
FROM python:3.12-alpine
#### 镜像来源 https://registry.hub.docker.com/_/python
LABEL maintainer "yxh <xianhe_yan@sina.com>"
ENV PY_VERSION=python3.12
#### 指定工作目录
WORKDIR /usr/src/app
COPY . .
COPY ./requirements.txt ./
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && \
    apk add --no-cache build-base libffi-dev openssl-dev && \
    pip install --upgrade pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN sed -i 's/https:\/\/cdn.jsdelivr.net\/npm\/swagger-ui-dist@5/\/static\/swagger-ui-5.8.0/g' /usr/local/lib/${PY_VERSION}/site-packages/fastapi/openapi/docs.py
RUN sed -i 's/https:\/\/fastapi.tiangolo.com\/img/\/static/g' /usr/local/lib/${PY_VERSION}/site-packages/fastapi/openapi/docs.py
EXPOSE 8000
#### 启动uvicorn 项目

CMD ["uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]

