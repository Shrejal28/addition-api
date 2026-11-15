# Project A — Addition API

A FastAPI application that accepts two numbers and returns their **sum**.  
Integrated with **Pytest** for testing, **Evidently** for data monitoring, and **Jenkins** for CI/CD.

---

## Project Structure

```
project_addition/
├── main.py                  # FastAPI application
├── test_main.py             # Pytest test suite
├── evidently_report.py      # Evidently monitoring report generator
├── requirements.txt         # Python dependencies
├── Jenkinsfile              # Jenkins CI/CD pipeline
├── reports/                 # Generated test & Evidently reports (auto-created)
└── README.md
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI server
```bash
uvicorn main:app --reload --port 8001
```

### 3. Test the API
- Swagger UI: http://127.0.0.1:8001/docs  
- GET request: http://127.0.0.1:8001/add?num1=10&num2=5  
- POST request body: `{"num1": 10, "num2": 5}`

---

## Run Tests (Pytest)
```bash
pytest test_main.py -v
```

---

## Generate Evidently Report
```bash
python evidently_report.py
# Opens reports/addition_evidently_report.html
```

---

## Jenkins Pipeline
1. Create a new Pipeline job in Jenkins.  
2. Point it to this repository/folder.  
3. Use the `Jenkinsfile` in this directory.  
4. Run the build — it will: install deps → lint → test → generate Evidently report → smoke test.
