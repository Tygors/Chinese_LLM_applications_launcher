## a simple demo about RAG using iFlyTek's Spark large language model.(real estate Q&A)

一个使用了科大讯飞大模型接口的检索增强小demo（房地产Q&A问答版）

easy to run via docker

----
### 启动方式
1. configs/config.py中填入科大讯飞接口的鉴权信息
```py
SPARK_ID = 'xxxxxxxx'
SPARK_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SPARK_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

2. 项目根目录下启动docker 注意最后有个英文句点 be ware of the period
```bash
docker build -t aname:v1 .
```

3. 启动
```bash
docker run -dp 7860:7860 --name acontainer aname:v1
```

### 演示
![演示截图](./overview.png "房地产QA问答版演示")

还有好多#TODO，缓慢更新中。to be continued...