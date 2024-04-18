



## 项目结构

~~~
.
├── controllers                  # 控制层 目录
│   └── auth_controllers.py
├── dev.env                      # 开发环境变量
├── docker-compose.yml           # docker yml
├── Dockerfile                   # Dockerfile
├── favicon.ico
├── logs                         # 日志目录
├── main.py                      # 主程序
├── modules                      # 模块目录
│   ├── db_client.py
│   └── module_route.py
├── public                       # 公共 目录
│   ├── get_logging.py           # 获取日志
│   ├── metadata.py              # 获取元数据
│   ├── schedule_job.py          # 定时任务
│   ├── system.py
│   └── utils_tools.py           # 工具类
├── README.md
├── requirements.txt
├── shell
├── sql                          # 脚本目录
│   └── user.sql
├── static                       # 静态资源目录
├── test
│   ├── ……
│   └── tt.py
├── run.bat                      # 运行脚本
├── run.sh                       # 运行脚本
├── test.bat                     # TestClient 测试脚本
├── test.sh                      # TestClient 测试脚本
└── TestClient.py                # 关于接口测试

~~~


_ main 文件主要是程序入口,将其他方法注册到主文件中.其他层托管其他地方处理.
- 添加接口 需要在 main 文件中注册 *控制层中的具体方法*
- 如：将controllers 目录下的auth_controllers文件中 auth_controllers_ping 方法注册到主方法中


~~~
## controllers
from controllers import auth_controllers
# 将controllers文件的函数注册到当前全局命名空间中
globals()[auth_controllers.auth_controllers_ping.__name__] = auth_controllers.auth_controllers_ping
~~~

- 将 auth_controllers_ping 绑定到接口中 (interfaces) 

~~~
INSERT INTO `interfaces` (transaction_id,name,path, method, controller,system_id,tags, description)
VALUES ('ZR00001','探针','/api/ping', 'GET', 'auth_controllers_ping','ZR0001','ping','测试系统探针');
~~~

- 以上添加 服务探针接口, 请求方式是 GET 请求路径为 /api/ping.具体请求参数在 auth_controllers_ping 方法中处理.
- 关于 controllers 层命名以文件名_具体方法名.禁止 controllers 中有重复的方法名及整改项目禁止方法名重复[原因工程使用方法名注入]

## 关于日志

### 使用 logure 中的 logger
   - 系统环境变量定义 LOG_LEVEL 设置logs 日志级别 debug info success error 默认DEBUG
   - 建设使用 source dev prod && 运行脚本
   ~~~
   echo "LOG_LEVEL=info">> ~/.bashrc
   ~~~
   - 日志存放位置在项目下的logs文件中


## 关于关系型数据库

### 关系数据库使用sqlalchemy orm 
   - 需要依赖pymysql
   - 需要创建 MySQLdb 别名以便与 SQLAlchemy 兼容 ORM
   ~~~
   # 以便与 SQLAlchemy 兼容 ORM
   import pymysql
   pymysql.install_as_MySQLdb() 
   ~~~
### 简单操作

~~~~~~
# # 插入数据
 new_entry = Route(transaction_id='xx',name='yy',……)
 session.add(new_entry)
 session.commit()
# # 查询数据
 results = session.query(Route).all()
# # 更新数据
 entry = session.query(Route).filter_by(transaction_id=1).first()
 entry.name = 'Updated Name'
 session.commit()
# # 删除数据
 entry = session.query(Route).filter_by(transaction_id=1).first()
 session.delete(entry)
 session.commit()
# # 分页查询
page_size = 20  # 每页的记录数
page_number = 1  # 页码,从1开始
# 计算偏移量
offset = (page_number - 1) * page_size
# 查询数据并进行分页
results = session.query(Route).offset(offset).limit(page_size).all()
# # 原生sql
 result = session.execute("SELECT * FROM interfaces WHERE name = :name", {"name": "张三"})
# # 查询关联表数据
 users_with_addresses = session.query(User, Address).filter(User.id == Address.user_id).all()
~~~~~~

## 关于非系型数据库

### 关系数据库使用 redis

## 文件名、类名和方法名的规范
### 文件名：

   文件名应该使用全小写字母.
   如果文件名包含多个单词,可以使用下划线(_)进行分隔.
### 类名：

   类名应使用驼峰命名法,即每个单词的首字母大写,不包含下划线.
   类名应该是一个名词或名词短语,而且应该具有描述性.
### 方法名：

   方法名应使用小写字母.
   如果方法名包含多个单词,可以使用下划线(_)进行分隔.

* 列如:

~~~~~~
# 文件名：my_module.py
class MyClass:
    def do_something(self):
        # 方法体
        pass

def my_function():
    # 函数体
    pass

~~~~~~

* 其他注意事项：
* 尽量避免使用缩写或简写,除非在广泛接受的情况下.使用有意义的名称来描述变量、常量和参数.

- 由于内网部署 FastAPI Swagger UI 打不开
- 原因使用外网静js css 态资源将静态资源下载到本地修改一下

- 如 Python 3.10.12 lib 默认库在~/.local/lib/python3.10/site-packages/fastapi/openapi/docs.py

- 修改 get_swagger_ui_html 、get_redoc_html
- 静态文件已经上传值 static 目录
* get_swagger_ui_html
~~~~~~
    swagger_js_url: str = "/static/swagger-ui-5.8.0/swagger-ui-bundle.js",
    swagger_css_url: str = "/static/swagger-ui-5.8.0/swagger-ui.css",
    swagger_favicon_url: str = "/static/favicon.png",
~~~~~~
* get_redoc_html
~~~~~~
    redoc_js_url: str = "/static/redoc-2.1.1/redoc.standalone.js",
    redoc_favicon_url: str = "/static/redoc-2.1.1/favicon.png",
~~~~~~



##　关于接口测试

### 接口测试工具
- TestCase.py 接口测试工具　pytest　Mock用于模拟
- 由于项目名字 fastapi 不能使用 pytest -k test_xxx　命令行运行
- 修改项目名称为 自己想要的目录名
* 比如 git clone -b default git@github.com:yanxianhe/vfastapi.git <项目名>

~~~~~~
    git clone -b default git@github.com:yanxianhe/vfastapi.git testproject
    pytest　TestClient.py　# 用于全接口测试
    pytest -k test_hello_world TestClient.py # 指定测试接口
    pytest -k test_hello_world --lf # 指定测试接口，只运行上次失败的接口
    pytest -k test_hello_world --ff # 指定测试接口，只运行上次失败的接口，并忽略依赖
~~~~~~

- 测试日志在项目 /logs/syslogs_2024-xx-xx.log
- 模拟测试 request.url 值 http://testserver/

- 备注
  - 项目找不目录可以手动指定
  ~~~~~~
      sys.path.insert(0, os.path.abspath("."))
  ~~~~~~
