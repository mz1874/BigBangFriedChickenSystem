# 注意, 为确保运行环境一致,在启动当前的项目之前使用下面命令同步开发环境
`pip install -r requirements.txt`


### 模型开始

- pip install flask-sqlalchemy
- pip install flask-migrate
- pip install pymysql
- 初始化数据库 `flask db init`
- 迁移 `flask db migrate`
- 更新 `flask db upgrade`
- 降级 `flask db downgrade`
- nohup gunicorn -w 4 -b 0.0.0.0:5000 App.app:app &