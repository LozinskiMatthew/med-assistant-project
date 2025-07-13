# 🔍 Advanced RAG System with Dual Backend Architecture for medical diagnosis

This project implements a large-scale, production-ready **Retrieval-Augmented Generation (RAG)** system, designed for modularity, scalability, and cloud-native deployment.

## 🧠 Overview

An advanced RAG system integrated within a **RESTful API**, using a **multi-container architecture** to maintain clean separation of concerns:

- **FastAPI**: Implements the RAG engine logic in its own container to ensure scalability and maintainability.
- **Django**: Handles user management and authentication, along with PostgreSQL for persistent storage.
- **Angular**: Frontend application for interacting with and displaying backend data.
- **PostgreSQL**: Relational database connected to the Django backend.

## ⚙️ Architecture
+----------------------+ +---------------------+ \
| Angular UI | <----> | FastAPI (RAG API) | <----> | Django (volume) | \
| Django (Users/Auth) | <----> | PostgreSQL DB | \
+----------------------+ +----------------------+


## 🚀 Features

- 🔁 **Dual Backend**: Django (auth, admin) & FastAPI (RAG inference)
- 🐳 **Full Dockerization**: All components containerized for reproducibility
- ⚙️ **CI/CD-Ready**: Jenkins pipelines configured for continuous integration & deployment
- ☁️ **Cloud Deployment**: Deployment targeted to Azure Kubernetes Service (AKS)
- 📈 **Monitoring (soon)**: Prometheus & Grafana support for live metrics and observability
- 🧠 **LLM Extensions**: Actively integrating advanced language model features

## 📦 Tech Stack

- **Backend**: FastAPI, Django, PostgreSQL
- **Frontend**: Angular
- **Orchestration**: Docker, Docker Compose
- **CI/CD**: Jenkins
- **Cloud**: Azure Kubernetes Service (AKS)
- **Monitoring** (upcoming): Prometheus, Grafana

---

## 🛠️ How to Run the Project

Running this project is extremely simple thanks to full Dockerization. The **entire application** (frontend, backend, vector engine, database) runs in containers — no need to install Python, Node.js, PostgreSQL, etc. on your machine.

> ⚠️ **Important:**  
> You must have Docker **Engine** running on your host (not Docker Desktop), due to the usage of **Docker-outside-of-Docker (DooD)** for internal builds.

---

### 🔧 Prerequisites

- [Docker Engine](https://docs.docker.com/engine/install/) installed and running  
- Basic terminal usage  
- Clone this repository

---

### 📂 Environment Setup

Before running the stack, you need to configure two `.env` files:

#### 1️⃣ Root `.env` (in the main project folder)

```env
POSTGRES_DB=medical                # must be 'medical'
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=postgres            # must be 'postgres'
POSTGRES_PORT=5432                # must be '5432'
COHERE_API_KEY=your_api_key
GROQ_API_KEY=your_api_key

Directly in the main forlder of the entire app, file .env:
POSTGRES_DB=medical #must be this
POSTGRES_USER=something_you_want
POSTGRES_PASSWORD=something_you_want
POSTGRES_HOST=postgres #must be this
POSTGRES_PORT=5432 #must be this
COHERE_API_KEY=your_api_key
GROQ_API_KEY=your_api_key

Then second .env dircetly in the rag folder with the following content:
COHERE_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
```

## 🔑 1.5 Get Your API Keys

To use the language models, you must generate and insert valid API keys:

    🧠 Cohere API Key

        Sign up or log in at: https://dashboard.cohere.com

        Go to the API Keys section

        Copy your key and replace your_api_key in the .env files

    ⚡ GROQ API Key

        Create an account at: https://console.groq.com/keys

        Generate a new key at this website

        Copy it and paste in both .env files where GROQ_API_KEY is needed

## 2️⃣ RAG `.env` (inside `/rag` folder)

Create a second `.env` file specifically for the RAG component with the following content:

```env
COHERE_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
```

## 🧱 First-Time Setup

Only one extra step is required before building the stack — install frontend dependencies:

```bash
cd frontend
npm install
```

## ▶️ Running the Full Stack

Once the `.env` files and frontend dependencies are set, simply run:

```bash
docker-compose up --build
```

This builds and runs the following services:

    Django backend for user management and PostgreSQL

    FastAPI container hosting the RAG logic

    Angular frontend exposed at http://localhost:4200

## ✅ That’s It!
You now have a fully running production-grade RAG system on your local machine — ready for:

    🔬 Experimentation

    🧪 Prototyping

    ☁️ Cloud deployment

    🤖 Extending with new LLM features

## 📌 Development Status

> 🛠️ Currently focused on stability improvements and LLM feature integration.  
> ☁️ Cloud deployment to AKS in progress.  
> 📊 Monitoring stack will be added soon.
 

Feel free to contribute, fork, or reach out if you'd like to collaborate!