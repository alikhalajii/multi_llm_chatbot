# <img src="assets/logo.png" width="40" style="vertical-align: middle;"/> Multi-LLM Chatbot

> ⚠️ **Work in Progress**: This project is in early development.  
> Features, structure, and documentation will evolve quickly.

A multilingual **retrieval-augmented chatbot** powered by [LangChain](https://github.com/langchain-ai/langchain), [Together AI](https://github.com/togethercomputer/together-python), [FastAPI](https://fastapi.tiangolo.com/), and [pgvector](https://github.com/pgvector/pgvector), with the ability to easily switch between different language models.


---

## Usage

### Option 1: Local Development
```bash
# 1. Create and activate a new virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install repo as a package
pip install -e .

# 3. Add your TogetherAI API key in the `.env` file

# 4. Start backend + frontend + db (hot reload)
make dev
```
### Option 2: Docker Compose
```bash
docker compose up --build
```

Backend API → http://localhost:8000/docs

Gradio UI   → http://localhost:7860


<h4 style="text-align: center;">Upload Document</h4>
<p style="text-align: center;">
  <img src="assets/demo_document_v0.2.1.png" alt="Documents" width="350" />
</p>

<h4 style="text-align: center;">Select Model and Chat</h4>
<p style="text-align: center;">
  <img src="assets/demo_chat_v0.2.0.png" alt="Chat" width="350" />
</p>
