import gradio as gr
from langchain.schema import HumanMessage
from app.core.pipeline import app, build_config
from app.models import TOGETHER_MODEL_MAP

MODEL_KEYS = list(TOGETHER_MODEL_MAP.keys())


def chatbot_fn(user_input, history, model_key):
    """ Gradio chatbot function to handle user input and generate responses."""
    config = build_config("together", model_key)
    input_messages = [HumanMessage(user_input)]
    output = app.invoke({"messages": input_messages}, config)
    answer = output["messages"][-1].content

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": answer})

    num_user_msgs = sum(1 for msg in history if msg["role"] == "user")
    height = "50vh" if num_user_msgs == 1 else None

    chat_data = [(msg["content"], None) if msg["role"] == "user" else (None, msg["content"]) for msg in history]

    if height:
        return history, gr.update(visible=True, value=chat_data, height=height), ""
    else:
        return history, gr.update(visible=True, value=chat_data), ""


with gr.Blocks(css="""
    body {
        background: linear-gradient(-45deg, #001F3F, #023562, #0F2027, #1A2980);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .gradio-container {
        width: 90%;
        max-width: 800px;
        min-height: 100vh;
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        overflow-y: auto;
    }

    #title {
        font-size: 22px;
        font-weight: bold;
        margin-top: 10px;
    }

    .gr-chatbot {
        background: linear-gradient(to bottom right, #e0f7fa, #ffffff);
        border: 2px solid #1A2980;
        border-radius: 12px;
        padding: 16px 16px 4px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        min-height: 100px;
        max-height: 80vh;
        overflow-y: auto;
        margin-bottom: 0;
        padding-bottom: 0;
    }

    .gr-textbox textarea {
        font-size: 16px;
        font-weight: bold;
        background-color: #ffffff;
        border-radius: 8px;
        border: 2px solid #0077cc;
        padding: 10px;
        box-shadow: 0 0 4px rgba(0,0,0,0.1);
        transition: border-color 0.3s ease;
    }

    .gr-textbox textarea:focus {
        border-color: #00bfa6;
        outline: none;
    }

    .gr-button {
        font-size: 16px;
        padding: 10px 20px;
    }

    #input-bar {
        position: sticky;
        bottom: 0;
        background: white;
        padding-top: 10px;
        z-index: 10;
    }

    .human-msg, .ai-msg {
        background-color: #f1f3f5;
        color: #000;
        padding: 10px 14px;
        border-radius: 12px;
        max-width: 95%;
        margin: 8px auto;
        margin-bottom: 0;
        padding-bottom: 0;
        line-height: 1.6;
        font-size: 16px;
        white-space: pre-wrap;
        word-break: break-word;
        display: block;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .human-msg {
        background-color: #d0ebff;
        border-left: 4px solid #0077cc;
    }

    .ai-msg {
        background-color: #f1f3f5;
        border-left: 4px solid #999;
    }

    @media (max-width: 768px) {
        .gradio-container {
            max-width: 100%;
            max-height: none;
            border-radius: 0;
            box-shadow: none;
            padding: 10px;
        }

        #title {
            font-size: 18px;
        }
    }
""") as demo:

    with gr.Row():
        with gr.Column(scale=6):
            gr.Image("assets/logo.png", show_label=False, width=80)
            gr.Markdown("### 🤖 Multi-Modell KI-Chatbot", elem_id="title")
        with gr.Column(scale=6):
            model_choice = gr.Dropdown(
                choices=MODEL_KEYS,
                value="llama_3_70b",
                label="Modell auswählen:",
                interactive=True
            )

    chatbot = gr.Chatbot(label="💬 Chatverlauf", visible=False)

    # add some vblank rows for spacing
    for _ in range(12):
        gr.Row()

    with gr.Row(elem_id="input-bar"):
        with gr.Column(scale=10):
            msg = gr.Textbox(
                placeholder="📝 Schreibe hier...",
                label="Was möchtest du sagen?",
                lines=1,
                max_lines=6,
                show_copy_button=False
            )
        with gr.Column(scale=2):
            send_btn = gr.Button("➤", variant="primary")

    state = gr.State([])

    send_btn.click(chatbot_fn, [msg, state, model_choice], [state, chatbot, msg])
    msg.submit(chatbot_fn, [msg, state, model_choice], [state, chatbot, msg])

if __name__ == "__main__":
    demo.launch(share=True)
