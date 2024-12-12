from flask import Flask, jsonify
from loguru import logger
import os
import sys
import multiprocessing
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(cur_dir))
from chat_ui.chatbot import launch_gradio

app = Flask(__name__)

@app.route("/",methods=["GET"])
def hello():
    return "hello"

@app.route("/heart_beat", methods=["GET","POST"])
def heart_beat():
    return jsonify(200)


if __name__ == "__main__":
    try:
        process = multiprocessing.Process(target=launch_gradio)
        process.start()
        logger.info("flask service start")
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error("fail to start the service: ",e)