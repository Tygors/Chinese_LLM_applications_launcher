import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import gradio as gr
from loguru import logger
import sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(cur_dir))
statistic_path = os.path.join(cur_dir, "images")
from splitter.text_split import gen_ans

def clear_session():
    """Clears the chat session."""
    return "", None

# def generate_chat(
#     input_text: str, history: list[list[str]], endpoint: str = CHAT_ENDPOINT
# ):
#     """Generates chat responses and updates the chat history."""

#     input_text = input_text or "你好"
#     history = (history or [])[-5:]  # Keep the last 5 messages in history

#     messages = []
#     for message, answer in history:
#         messages.append({"role": "user", "content": message})
#         if answer:
#             messages.append({"role": "assistant", "content": answer})

#     # append latest message
#     stream_response = chat_stream_generator(
#         messages=messages, endpoint=endpoint, temperature=0.2
#     )
#     for character in stream_response:
#         history[-1][1] += character
#         yield None, history
#     else:
#         yield None, history

def validate_field_word_count(
    input_text: str, description: str, max_word_count: int = 3000
):
    """
    Validate the input text for word count

    :param input_text:
    :return:
    """
    if len(input_text) == 0:
        raise gr.Error(f"{description}不能为空")

    if len(input_text) > max_word_count:
        raise gr.Error(f"{description}字数不能超过{max_word_count}字")
    
def validate_chat(input_text: str):
    """
    Validate the input text

    :param input_text:
    :return:
    """
    validate_field_word_count(input_text, "输入", 500)

# def launch_gradio():
    # with gr.Blocks() as demo:
    #     gr.Markdown("输入你的问题并点击 **开始RAG** 可以检索增强回答。（上下文todo）")
    #     with gr.Row():
    #         inp = gr.Textbox(placeholder="输入你想问的关于销售QA的问题")
    #         out = gr.Textbox()
    #     btn = gr.Button("开始RAG")
    #     btn.click(fn=gen_ans, inputs=inp, outputs=out)
    # logger.info("gradio service start")
    # demo.launch(server_name="0.0.0.0")
with gr.Blocks(
    title="Tygors",
    # theme="shivi/calm_seafoam@>=0.0.1,<1.0.0",
) as demo:

    def user(user_message, history):
        return user_message, (history or []) + [[user_message, ""]]

#     gr.Markdown(
#         """
#         <div style="overflow: hidden;color:#fff;display: flex;flex-direction: column;align-items: center; position: relative; width: 100%; height: 180px;background-size: cover; background-image: url(https://cdn.pixabay.com/photo/2021/09/12/07/58/banner-6617550_1280.png);">
#             <img style="width: 130px;height: 60px;position: absolute;top:10px;left:10px" src="https://img.icons8.com/?size=256w&id=aqokH1kNs0rl&format=png"/>
#             <img style="min-width: 1416px; width: 1416px;height: 100px;margin-top: 30px;" src="https://cdn.pixabay.com/photo/2014/04/02/10/19/ribbon-303449_1280.png"/>
#         </div>
# """
#     )
    with gr.Tab("房产chitchat"):
        chatbot = gr.Chatbot(
            label="sparkLLM",
            elem_classes="control-height",
            show_copy_button=True,
            min_width=1368,
            height=416,
        )
        chat_text_input = gr.Textbox(label="输入", min_width=1368)

        with gr.Row():
            with gr.Column(scale=2):
                gr.Examples(
                    [
                        "其他费用包括哪些",
                        "能给到哪些优惠呢",
                        "附近有什么好学校",
                        "我比较担心物业跟不上",
                        "建筑质量如何",
                    ],
                    chat_text_input,
                    label="可以问问我：",
                )
            with gr.Column(scale=1):
                with gr.Row(variant="compact"):
                    clear_history = gr.Button(
                        "清除历史",
                        min_width="17",
                        size="sm",
                        scale=1,
                        icon=os.path.join(statistic_path, "clear.png"),
                    )
                    submit = gr.Button(
                        "发送",
                        variant="primary",
                        min_width="17",
                        size="sm",
                        scale=1,
                        icon=os.path.join(statistic_path, "arrow_up.png"),
                    )

        chat_text_input.submit(
            fn=validate_chat, inputs=[chat_text_input], outputs=[], queue=False
        ).success(
            user, [chat_text_input, chatbot], [chat_text_input, chatbot], queue=False
        ).success(
            fn=gen_ans,
            inputs=[chat_text_input, chatbot],
            outputs=[chat_text_input, chatbot],
        )

        submit.click(
            fn=validate_chat, inputs=[chat_text_input], outputs=[], queue=False
        ).success(
            user, [chat_text_input, chatbot], [chat_text_input, chatbot], queue=False
        ).success(
            fn=gen_ans,
            inputs=[chat_text_input, chatbot],
            outputs=[chat_text_input, chatbot],
            api_name="chat",
        )
        clear_history.click(
            fn=clear_session, inputs=[], outputs=[chat_text_input, chatbot], queue=False
        )

    # with gr.Tab("基于文档问答"):

def launch_gradio():
    demo.queue(api_open=False, max_size=40).launch(
            height=800,
            share=False,
            server_name="0.0.0.0",
            show_api=False,
            max_threads=4,
        )


if __name__ == "__main__":
    launch_gradio()