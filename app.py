from dotenv import load_dotenv

load_dotenv()

import gradio as gr
from chat_caller import query_gpt_chat, check_quota_status, choose_model
from chat_utils import read_course_assets
import os

from brand_theming import customtheme


def call_chat(query, chat_history):
    # unpack history
    chat_history_unpacked = []
    for x in chat_history:
        for y in x:
            chat_history_unpacked.append(y)
    chat_engine, answer = query_gpt_chat(query, chat_history_unpacked)
    chat_history.append((query, answer))
    return "", chat_history


# with gr.Blocks() as demo:
with gr.Blocks(theme=customtheme, analytics_enabled=False, title="Pruju AI") as demo:

    examples, chat_header, chat_footer = read_course_assets()

    gr.Markdown(value=chat_header)
    chatbot = gr.Chatbot(
        label="Model: " + choose_model(check_quota_status()),
        scale=10,
        show_label=True,
        bubble_full_width=False,
        show_copy_button=True,
    )
    with gr.Group():
        with gr.Row():
            query = gr.Textbox(
                show_label=False,
                placeholder="Your question.",
                scale=40,
                container=False,
                autofocus=True,
            )
            clear = gr.ClearButton(
                [query, chatbot], value="🗑️", scale=1, min_width=10, variant="secondary"
            )
            submit_button = gr.Button(
                value="Go!", scale=6, variant="primary", min_width=10
            )

    gr.Markdown(value=chat_footer)
    gr.Examples(examples=examples, inputs=query)
    query.submit(fn=call_chat, inputs=[query, chatbot], outputs=[query, chatbot])
    submit_button.click(
        fn=call_chat,
        concurrency_limit=int(os.getenv("MAX_CONCURRENCY")),
        inputs=[query, chatbot],
        outputs=[query, chatbot],
    )

if __name__ == "__main__":
    print("Launching Demo\n")
    server_name = "127.0.0.1"
    isDocker = os.path.exists("/.dockerenv")
    print(f"Docker: {isDocker}\n")

    demo.queue(max_size=int(os.getenv("MAX_QUEUE")))
    demo.launch(
        server_name="0.0.0.0" if isDocker else "127.0.0.1",
        root_path="/prujuai",
        show_api=False,
        favicon_path=os.getenv("CHAT_DATA_FOLDER") + "/favicon.ico",
    )
