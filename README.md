# <img src="assets/logo.png" width="40" style="vertical-align: middle;"/> Multi-LLM Chatbot

> ⚠️ **Work in Progress**: This project is in early development.  
> Features, structure, and documentation will evolve quickly.

A multilingual **retrieval-augmented chatbot** powered by [LangChain](https://github.com/langchain-ai/langchain), [Together AI](https://github.com/togethercomputer/together-python), [FastAPI](https://fastapi.tiangolo.com/), and [pgvector](https://github.com/pgvector/pgvector), with the ability to easily switch between different Language models.


---

## Usage

```bash
# 1. Create and activate a new virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install repo as a package
pip install -e .

# 3. Add your TogetherAI API key in the `.env` file

# 4. Start PostgreSQL + pgvector
docker compose up -d

# 5. Run FastAPI backend
uvicorn app.main:app --reload
# Docs available at: http://localhost:8000/docs

# 6. Run Gradio frontend
python app/gradio_app.py
```
**Open http://127.0.0.1:7860**

---
<h4 style="text-align: center;">Upload Document</h4>
<p style="text-align: center;">
  <img src="assets/demo_document_v0.2.0.png" alt="Upload Document Demo" width="350" />
</p>

<h4 style="text-align: center;">Select Model and Chat</h4>
<p style="text-align: center;">
  <img src="assets/demo_chat_v0.2.0.png" alt="Model Selection Demo" width="350" />
</p>

