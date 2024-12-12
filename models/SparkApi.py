from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import sys
import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.dirname(cur_dir))
from configs.config import SPARK_ID, SPARK_KEY, SPARK_SECRET

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
# 要换成自己的
SPARKAI_APP_ID = SPARK_ID
SPARKAI_API_SECRET = SPARK_SECRET
SPARKAI_API_KEY = SPARK_KEY
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = '4.0Ultra'

if __name__ == '__main__':
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content='你好呀'
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    print(a)
    # generations=[[ChatGeneration(text='您好！有什么可以帮助您的吗？', message=AIMessage(content='您好！有什么可以帮助您的吗？'))]] llm_output={'token_usage': {'question_tokens': 2, 'prompt_tokens': 2, 'completion_tokens': 7, 'total_tokens': 9}} run=[RunInfo(run_id=UUID('xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'))] 
    print(a.generations[0][0].message.content)
    # 您好！有什么可以帮助您的吗？