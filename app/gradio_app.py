import gradio as gr
import requests
import os
from typing import Any, List, Tuple

from app.llms import TOGETHER_MODEL_MAP, DEFAULT_MODELS

API_URL = os.getenv("API_URL", "http://localhost:8000")


def upload_docs(file_paths: list[str]) -> str:
    """Upload multiple text files to the backend API."""
    if not file_paths:
        return "No file selected"
    if not isinstance(file_paths, list):
        file_paths = [file_paths]

    files_to_send = []
    for path in file_paths:
        with open(path, "rb") as f:
            content = f.read()
            files_to_send.append(
                ("files", (os.path.basename(path), content, "text/plain"))
            )

    try:
        response = requests.post(f"{API_URL}/document/", files=files_to_send)
        return response.text
    except Exception as e:
        return f"Upload failed: {e}"


def list_docs() -> list[list[str]]:
    """Fetch docs as a list of rows for a DataFrame."""
    response = requests.get(f"{API_URL}/document/")
    if response.status_code != 200:
        return [["Error", response.text, ""]]

    docs = response.json()
    if not docs:
        return []

    # Add a "Select" column with False by default
    rows = [[False, d["id"], d["filename"], d["content_preview"]] for d in docs]
    return rows


def delete_selected(rows: list[list[str]]) -> tuple[str, list[list[str]]]:
    """Delete all docs that were selected in DataFrame."""
    # If DataFrame → convert to list of lists
    if hasattr(rows, "to_numpy"):  # pandas.DataFrame
        rows = rows.to_numpy().tolist()

    if not rows:
        return "No documents in list", list_docs()

    deleted = []
    errors = []
    for row in rows:
        if row[0]:  # first column = checkbox
            doc_id = int(row[1])
            res = requests.delete(f"{API_URL}/document/{doc_id}")
            if res.status_code == 200:
                deleted.append(doc_id)
            else:
                errors.append(f"{doc_id} (status {res.status_code})")

    msg = ""
    if deleted:
        msg += f"✅ Deleted: {deleted}\n"
    if errors:
        msg += f"⚠️ Errors: {errors}\n"
    if not msg:
        msg = "No docs selected"

    return msg, list_docs()


def chat_fn(
    user_input: str, history: List[dict[str, Any]], model_key: str
) -> Tuple[List[dict[str, Any]], List[dict[str, Any]], str]:
    user_input = user_input if isinstance(user_input, str) else " ".join(user_input)

    payload = {"user_input": user_input, "history": history, "model_key": model_key}
    response = requests.post(f"{API_URL}/chat/", json=payload)

    if response.status_code != 200:
        history.append(
            {
                "role": "assistant",
                "content": f"Error {response.status_code}: {response.text}",
            }
        )
        return history, history, ""

    data = response.json()
    return data["history"], data["history"], ""


with gr.Blocks(
    css="""
    body {
        background: linear-gradient(-45deg, #001F3F, #023562, #0F2027, #1A2980);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Segoe UI', sans-serif;
    }

    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .gr-button {
        font-size: 16px !important;
        padding: 10px 20px !important;
        border-radius: 12px !important;
    }

    .gr-textbox, .gr-file, .gr-dropdown {
        border-radius: 12px !important;
    }

    #logo {
        display: block;
        margin: 0 auto 10px auto; /* top: 0, right/left: auto, bottom: 10px */
        width: 100px; /* or whatever size works best */
    }

    #input-bar {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 10px;
        z-index: 10;
        border-top: 2px solid #ccc;
    }

    #subtitle {
        text-align: center;
        font-size: 14px;
        color: #333;
        margin-top: 5px;
        font-family: 'Arial', sans-serif;
    }

    .powered-by {
        font-size: 10px;
        color: #777;
        display: block;
        margin-top: 2px;
    }

    #send-btn button {
        background: linear-gradient(90deg, #ff007f, #ff9900, #00ffcc, #3399ff, #cc33ff);
        color: white;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        border-radius: 6px;
        cursor: pointer;
        transition: transform 0.2s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    #send-btn button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.3);
    }

"""
) as demo:
    with gr.Column():
        gr.Image("assets/logo.png", elem_id="logo", show_label=False)

    gr.HTML(
        """
        <div id="subtitle">
            Multi-LLM Chatbot<br>
            <span class="powered-by">powered by Langchain, FastAPI, PGVector</span>
        </div>
    """
    )

    with gr.Tab("Documents"):
        file_input = gr.File(
            file_types=[".txt"], type="filepath", label="Upload .txt files"
        )
        upload_button = gr.Button("Upload")
        upload_output = gr.Textbox()

        docs_table = gr.DataFrame(
            headers=["Select", "ID", "Filename", "Preview"],
            datatype=["bool", "number", "str", "str"],
            interactive=True,
            row_count=(0, "dynamic"),
            col_count=(4, "fixed"),
        )
        refresh_button = gr.Button("Refresh List")
        delete_button = gr.Button("Delete Selected")
        delete_output = gr.Textbox()

        upload_button.click(upload_docs, inputs=file_input, outputs=upload_output).then(
            list_docs, outputs=docs_table
        )
        refresh_button.click(list_docs, outputs=docs_table)
        delete_button.click(
            delete_selected, inputs=docs_table, outputs=[delete_output, docs_table]
        )

    with gr.Tab("Chat"):
        model_choice = gr.Dropdown(
            choices=list(TOGETHER_MODEL_MAP.keys()),
            value=DEFAULT_MODELS["together"],  # default selection
            label="Choose a Chat Model",
        )

        chatbot = gr.Chatbot(label="Chat", type="messages")
        state = gr.State([])
        with gr.Row(elem_id="input-bar"):
            msg = gr.Textbox(
                placeholder="Type your message here...", scale=4, show_label=False
            )
            send_btn = gr.Button("Send", elem_id="send-btn", scale=1)

        send_btn.click(chat_fn, [msg, state, model_choice], [state, chatbot, msg])
        msg.submit(chat_fn, [msg, state, model_choice], [state, chatbot, msg])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
