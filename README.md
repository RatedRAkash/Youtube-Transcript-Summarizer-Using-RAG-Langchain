# Youtube Transcript Summarizer using RAG

This is a complete end-to-end application that summarizes YouTube videos by extracting their transcripts and utilizing a **Retrieval-Augmented Generation (RAG)** pipeline.

---

## Demo Images of the Application

![website_demo1](./website_demo1.png)  
![website_demo2](./website_demo2.png)  

---

## Key Features

- Fetches video transcripts using the `Youtube Transcript Api`
- Generates local embeddings using `nomic-embed-text` via **Ollama**
- Uses **LLaMA 3.1 (8B)** model locally via Ollama for summarization and question answering
- RAG pipeline built using **LangChain**
- Stores vector representations using **FAISS** for fast semantic similarity search
- Serves output through a **Django API**
---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/youtube-transcript-summarizer.git
cd youtube-transcript-summarizer
```

### 2. Create and Activate Virtual Environment and install dependencies
```bash
python3 -m venv my_venv
source my_venv/bin/activate
pip install -r requirements.txt
```

### 3. Setting up Ollama Model
a) Install Ollama
Download and install Ollama from the official website: https://ollama.com

b) Pull Required Models
Run the following commands to pull the models used in this project:
```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b
```

c) Start Ollama Server:
```bash
ollama serve
```

d) Configure with appropriate variables in `.env` of the `youtube_transcript_RAG_model` model:
```bash
LLM_MODEL = "llama3.1:8b"
EMBEDDING_MODEL_NAME = "nomic-embed-text"
EMBEDDING_MODEL_API_URL = "http://localhost:11434/api/embeddings"
VECTOR_DATABASE_MODEL_PATH = "saved_model_faiss_store"
FINAL_QUESTION = "Can you summarize the video"
```

### 4. Start Django Server
At first generate the Static Folders to serve static contents:
```bash
cd youtube_transcript_django_backend
python manage.py collectstatic
```

Now start Django Server via `Gunicorn`:
```
gunicorn youtube_transcript_django_backend.wsgi:application --bind 0.0.0.0:8999
```