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
- **Testing**: Pytest
- **Logging**: Python Logging
- **Deployment**: Docker

## Folder Structure
Below is the structured layout of the project:

```
rag_qna_project/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── e117fe54c208_initial_migration.py
├── alembic.ini
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── document_ingestion.py
│   │   ├── document_selection.py
│   │   ├── question_answering.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db_models.py
│   │   ├── embedding_store.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embedding_service.py
│   │   ├── retrieval_service.py
│   ├── tests/
│       ├── __init__.py
│       ├── test_document_ingestion.py
│       ├── test_document_selection.py
│       ├── test_question_answering.py
├── configs/
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
├── docs/
│   ├── API_DOCS.md
│   ├── README.md
├── requirements.txt
├── sample_data/
│   └── sample.txt
```

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

## Running the Dockerized RAG Q&A Project

### 1️⃣ Pull the Latest Docker Image

Run the following command to pull the latest image from Docker Hub:

```sh
docker pull ashishkumar16/rag_qna_project:latest
```

### 2️⃣ Verify the Downloaded Image
To check if the image has been successfully pulled:

```sh
docker images
```

### 3️⃣ Download the docker-compose.yml file
Download the `docker-compose.yml` from the `/deployment` folder.

### 4️⃣ Start the Containers Using Docker Compose
Run the following command to start the FastAPI app and PostgreSQL database in detached mode:

```sh
docker-compose up -d
```

### 5️⃣ Check Running Containers
To verify if the containers are running:

```sh
docker ps
```

### 6️⃣ View Logs of the FastAPI App
To monitor the logs of the FastAPI application:

```sh
docker logs -f fastapi_app
```

### 7️⃣ Apply Database Migrations
Run the Alembic migrations inside the FastAPI container:

```sh
docker exec -it fastapi_app alembic upgrade head
```

### 8️⃣ Verify Database Tables
To check if the necessary tables exist inside PostgreSQL:

```sh
docker exec -it postgres_db psql -U postgres -d rag_db -c "\dt"
```

## ✅ Your RAG Q&A System is Now Running!
You can now access the FastAPI application at:

```
http://localhost:8000/docs or http://0.0.0.0:8000/docs
```

This will open the Swagger API documentation, where you can test the endpoints.

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
