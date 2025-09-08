# <img src="assets/logo.png" width="40" style="vertical-align: middle;"/> Multi-LLM Chatbot


> **⚠️ Under Development:** This is the initial commit and represents the very first step of the project.  
> Features, structure, and documentation will evolve quickly.


A multi–Large Language Model chatbot built with [LangChain](https://github.com/langchain-ai/langchain) and [Together AI](https://github.com/togethercomputer/together-python).  
Easily switch between different LLM backends and interact through a simple [Gradio](https://gradio.app/) web interface.


---

## Usage

**Create and activate a new virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate
```
**Install repo as a package**
```bash
pip install -e .
```
Make sure you have placed your TogetherAI API key in the `.env` file to access more models.

**Run the demo**
```bash
python app/gradio_app.py
```

---

<h4 style="text-align: center;">Model Selection</h4>

<p align="center">
  <img src="assets/demo_llms.png" alt="Model Selection" width="350"/>
</p>

<h4 style="text-align: center;">Multilingual Multi‑Model Chatbot Demo v0.1.0</h4>

<p align="center">
  <img src="assets/demo_v0.1.0.png" alt="Demo" width="350"/>
</p>
