# API Documentation  

This document provides details on the APIs for document ingestion, selection, and question answering. Additionally, it includes instructions on running tests, checking test coverage, and using Swagger UI for API exploration. 🚀

---

## **1️⃣ Upload Document**  

**Endpoint:**  
`POST /upload/`  

**Description:**  
Uploads a document and generates an embedding.  

### **Request**  
```bash
curl -X 'POST' 'http://127.0.0.1:8000/upload/' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-F 'file=@sample.txt'
```

### **Response**  
```json
{
    "message": "Document uploaded successfully",
    "document_id": 1
}
```

---

## **2️⃣ Select Documents**  

**Endpoint:**  
`POST /select_documents/`  

**Description:**  
Fetches documents based on provided IDs.  

### **Request**  
```bash
curl -X 'POST' 'http://127.0.0.1:8000/select_documents/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"doc_ids": [1,2,3]}'
```

### **Response**  
```json
{
    "selected_documents": [1,2,3]
}
```

---

## **3️⃣ Question Answering**  

**Endpoint:**  
`POST /qa/`  

**Description:**  
Answers a user's question by retrieving relevant documents.  

### **Request**  
```bash
curl -X 'POST' 'http://127.0.0.1:8000/qa/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"question": "What is AI?"}'
```

### **Response**  
```json
{
    "answer": "Artificial Intelligence is the simulation of human intelligence processes by machines."
}
```

---

## **4️⃣ API Documentation using Swagger UI**  

To explore and test APIs interactively, use Swagger UI.

### **How to Access Swagger UI**  
1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Open your browser and go to:
   ```
   http://127.0.0.1:8000/docs
   ```
3. Here, you can see all API endpoints, send requests, and check responses.

Alternatively, you can access **ReDoc** API documentation at:
   ```
   http://127.0.0.1:8000/redoc
   ```

---

## **5️⃣ Running Tests & Checking Test Coverage**  

### **Run All Tests**  
Execute the following command to run all test cases:
```bash
PYTHONPATH=$(pwd) pytest app/tests --disable-warnings
```

### **Run Tests with Coverage**  
To check test coverage, use:
```bash
PYTHONPATH=$(pwd) pytest app/tests --cov=app --disable-warnings
```

### **Test Coverage Report**  
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
