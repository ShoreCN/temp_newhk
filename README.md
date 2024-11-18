# 项目说明
- 项目设计
  - 产品定位
    - 目标用户为刚来到香港开始新的学习/生活/工作的人群, 解决此类用户在日常生活中难以获取信息,不知如何解决问题, 需要查询数据或者攻略的需求
  - 产品功能
    - 提供资讯(information)和攻略(guide)两大功能, 资讯主要新闻/热门排行/热点优惠之类的实时内容, 攻略主要提供证件办理/政府事务申请指南之类的固定内容

## 项目结构
- 后端服务 (Backend Services)
  - information-service: 资讯服务,提供新闻、热点、优惠等实时内容
  - guide-service: 攻略服务,提供各类固定指南内容
  - user-service: 用户服务,处理用户认证、授权等
  - api-gateway: API网关,统一管理服务访问
  
- 技术栈 (Tech Stack)
  - 框架: FastAPI
  - 数据库: MongoDB (文档存储), Redis (缓存)
  - 部署: Docker + Docker Compose
  
- 项目特点
  - 微服务架构,服务解耦
  - API网关统一管理
  - 异步处理提升性能
  - 分布式缓存加速访问
  - 容器化部署便于扩展

- 开发规范
  - 代码规范遵循PEP8
  - API文档使用OpenAPI规范
  - Git分支管理采用GitFlow
  - 单元测试覆盖率>80%
  - 代码审查制度

## 项目启动方式

### 本地开发环境启动

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 启动docker容器
```bash
docker compose up -d
```

3. 启动后端服务
```bash
uvicorn app.main:app --reload
```

4. 访问API文档
```bash
http://localhost:8000/docs
```



