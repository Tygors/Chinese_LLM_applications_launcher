FROM python:3.9.20
# FROM llm_apps:v1
WORKDIR /usr/src/app
ENV HF_ENDPOINT=https://hf-mirror.com
COPY ./nltk_data /root/nltk_data
COPY . .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip install -U huggingface_hub

EXPOSE 8080 7860
ENTRYPOINT ["python","api/server.py"]