# RAG-Based Q&A System

## Overview
This project is a **RAG (Retrieval-Augmented Generation) based Q&A system** that allows users to **upload documents, select relevant ones, and ask questions**. The system utilizes **FAISS** for vector search, **FastAPI** for API development, and **PostgreSQL** for structured data storage.

## Features
- **Document Ingestion**: Upload text documents and generate vector embeddings.
- **Document Selection**: Select relevant documents from the stored database.
- **Question Answering**: Retrieve relevant document passages based on the question.
- **FastAPI Integration**: Provides interactive API documentation with Swagger.
- **Test Coverage**: Achieved **83%+** test coverage with `pytest`.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Vector Search**: FAISS
- **Database**: PostgreSQL
- **Embedding Models**: SentenceTransformers
- **Testing**: Pytest, Coverage.py
- **Logging**: Python Logging
- **Deployment**: Docker

---

## **Installation Steps**
Follow these steps to set up and run the project.

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/rag_qna_project.git
cd rag_qna_project
```

### 2️⃣ Create a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables
Create a `.env` file in the `configs/` directory:
```sh
touch configs/.env
```
Add the following configurations:
```ini
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 5️⃣ Start PostgreSQL (If not running)
Make sure PostgreSQL is installed and running.

For Mac:
```sh
brew services restart postgresql
```

### 6️⃣ Run Migrations
```sh
alembic upgrade head
```

### 7️⃣ Start the API Server
```sh
uvicorn app.main:app --reload
```

## API Access  

Once the server is running, you can access:  

- **API Base URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## **Testing**
Run the test suite with coverage:
```sh
PYTHONPATH=$(pwd) pytest app/tests --cov=app --disable-warnings
```

### ✅ Current Coverage:
```text
================================================ test session starts ================================================
platform darwin -- Python 3.10.16, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/ashish/Desktop/JK_Tech/rag_qna_project
plugins: cov-6.0.0, anyio-4.8.0
collected 3 items                                                                                                    

app/tests/test_document_ingestion.py .                                                                        [ 33%]
app/tests/test_document_selection.py .                                                                        [ 66%]
app/tests/test_question_answering.py .                                                                        [100%]

--------- coverage: platform darwin, python 3.10.16-final-0 ----------
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
app/api/__init__.py                          0      0   100%
app/api/document_ingestion.py               30      4    87%
app/api/document_selection.py               25      4    84%
app/api/question_answering.py               31      5    84%
app/core/__init__.py                         0      0   100%
app/core/config.py                           4      0   100%
app/core/logging_config.py                   3      0   100%
app/main.py                                 12      2    83%
app/models/__init__.py                       0      0   100%
app/models/db_models.py                     18      2    89%
app/models/embedding_store.py               42     12    71%
app/models/embedding_store_instance.py       2      0   100%
app/services/__init__.py                     0      0   100%
app/services/embedding_service.py           11      3    73%
app/services/retrieval_service.py           22      5    77%
app/tests/__init__.py                        0      0   100%
app/tests/test_document_ingestion.py         7      0   100%
app/tests/test_document_selection.py         6      0   100%
app/tests/test_question_answering.py         7      0   100%
------------------------------------------------------------
TOTAL                                      220     37    83%
=========================================== 3 passed, 5 warnings in 8.36s ===========================================
```
---
