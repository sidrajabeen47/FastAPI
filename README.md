# FastAPI
# 🚀 Generative AI Task Architecture Engine

An intelligent, asynchronous REST API that bridges the gap between abstract human goals and structured database states. By combining **FastAPI** with **LangChain**, the engine automatically deconstructs macro-objectives into granular, actionable tasks, parsing unstructured AI completions into structured data arrays instantly.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI (Asynchronous, Pydantic data validation, automated Swagger UI)
* **AI Orchestration:** LangChain Core (`ChatOpenAI` wrapper via Hugging Face Router)
* **LLM Model:** Mistral-7B-Instruct-v0.2
* **Database & ORM:** SQLite managed via SQLAlchemy

---

## ✨ Key Features

* **Automated AI Pipeline:** Integrated LangChain and Mistral-7B to orchestrate strict prompting and parse unstructured text completions into valid data arrays.
* **Strict Schema Validation:** Utilized Pydantic models (`TaskCreate`, `TaskUpdate`, `GoalRequest`, `Task`) to enforce dual-layer type safety across all client requests and AI-generated payloads.
* **Decoupled ORM Design:** Architected clean, context-managed database connections (`get_db`) using SQLAlchemy to ensure optimal connection handling.
* **Production-Ready CRUD:** Built a full suite of standardized HTTP endpoints (`GET`, `POST`, `PUT`, `DELETE`) with a self-documenting interactive UI.

---

## 📂 Project Structure

```text
├── database.py      # Database configuration and session manager (get_db)
├── models.py        # SQLAlchemy relational database models
├── schemas.py       # Pydantic data validation schemas
├── main.py          # FastAPI application routes and AI orchestration logic
├── tasks.db         # SQLite local database instance
├── .env             # Environment variables (API tokens)
└── requirements.txt # Project dependencies
