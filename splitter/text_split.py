# https://blog.csdn.net/C_JackForme/article/details/140236923

from langchain.vectorstores import Chroma, FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from loguru import logger
import sys
import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(cur_dir))
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from models.SparkApi import *

loader = DirectoryLoader("./splitter/", glob="*.txt")

documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)

split_docs = text_splitter.split_documents(documents)

model_name = "shibing624/text2vec-base-chinese-sentence"#/distiluse-base-multilingual-cased-v1"

embeddings = HuggingFaceBgeEmbeddings(model_name=model_name)

# docsearch = Chroma.from_documents(
#     split_docs,
#     embeddings,
#     persist_directory="./vector_store"
# )
# docsearch.persist()

# # 加载数据
# docsearch = Chroma(persist_directory="./vector_store",embedding_function=embeddings)

def datas_to_embeddings(docs, db_name, embeddings):
    """使用 Faiss 作为向量数据库，持久化存储房产销售 问答对（QA-Pair）"""
    try:
        db = FAISS.from_documents(docs, embedding=embeddings)

        if not os.path.exists(db_name):  # 向量数据库文件不存在就创建并保存
            db.save_local(db_name)
        else:
            old_db = FAISS.load_local(db_name, embeddings=embeddings,allow_dangerous_deserialization=True)  # 向量数据库文件存在就添加并保存
            old_db.merge_from(db)
            old_db.save_local(db_name)
        return True
    except Exception as e:
        raise e
    
def split_datas(file_datas, split_str=r'\n\n---\n\n'):
    """文本拆分"""
    text_splitter = CharacterTextSplitter(
        separator=split_str,
        chunk_size=150,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=True,
    )
    docs = text_splitter.create_documents([file_datas])
    print(docs[1])
    return docs

def read_file(file_name):
    """读取文本"""
    with open(file_name,encoding="utf-8") as f:
        file_datas = f.read()
    return file_datas

def query_db(db_name, query):
    """使用 Faiss 作为向量数据库，去向量数据里做内容检索"""
    db = FAISS.load_local(db_name, embeddings,allow_dangerous_deserialization=True)
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.1, 'k': 1, "fetch_k": 2}  # 按相关性去查找, k默认返回几条

    )
    docs = retriever.get_relevant_documents(query)
    if docs:
        for d in docs:
            return d.page_content.split("：**")[-1]
    else:
        return "没有符合条件的回答"


def portal(file_name, db_name, split_str):
    """
    主函数：读取文本、分割文本、向量化、存到向量数据库
    """
    file_datas = read_file(file_name)
    docs = split_datas(file_datas, split_str)
    res = datas_to_embeddings(docs, db_name, embeddings)
    return res

def gen_ans(input_text: str, history: list[list[str]], db_name="faiss_vecs"):
    history = (history or [])[-5:]
    logger.info(f"从输入框获取到输入为:{input_text}")
    raw_input = input_text
    db = FAISS.load_local(db_name, embeddings,allow_dangerous_deserialization=True)
    similar_docs = db.similarity_search(input_text,k=1)
    info = ""
    for similar_doc in similar_docs:
        info = info + similar_doc.page_content
    input_text = "结合以下信息：" + info + "\n\n请严格遵循以上提供的销售回答内容，请完整提取出销售回答的内容来回答以下问题：" + input_text
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
        content=input_text
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    ans = a.generations[0][0].message.content
    logger.info(f"输出到输出框的结果为:{ans}")
    history[-1][1] = ans
    return None, history

if __name__ == "__main__":
    question = "建筑质量怎么样呢"
    """
    similar_docs = docsearch.similarity_search(question, k=4)
    info = ""
    print("----------------------------------")
    for similar_doc in similar_docs:
        info = info + similar_doc.page_content
    question = "结合以下信息：" + info + "回答" + question
    print("----------------------------------")
    print(question)
    print("----------------------------------")
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
        content=question
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    print(a.generations[0][0].message.content)
    """
    db_name="faiss_vecs"
    #print(portal(r"D:\python_internship\launch_some_LLM_applications\splitter\real_estate_sales_data.txt",db_name,"---"))
    db = FAISS.load_local(db_name, embeddings,allow_dangerous_deserialization=True)
    #print(query_db(db_name,"你们的售后服务如何"))
    similar_docs = db.similarity_search(question,k=1)
    info = ""
    print("----------------------------------")
    for similar_doc in similar_docs:
        info = info + similar_doc.page_content
    question = "结合以下信息：" + info + "\n\n请严格遵循以上提供的销售回答内容，请完整提取出销售回答的内容来回答以下问题：" + question
    print("----------------------------------")
    print(question)
    print("----------------------------------")
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
        content=question
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    print(a.generations[0][0].message.content)
