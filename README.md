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

## 📌 Development Status

> 🛠️ Currently focused on stability improvements and LLM feature integration.  
> ☁️ Cloud deployment to AKS in progress.  
> 📊 Monitoring stack will be added soon.

---

Feel free to contribute, fork, or reach out if you'd like to collaborate!
