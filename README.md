<h1 align="left">
DocIntell
</h1>

<h3 align="left">
Intelligent Document Processing Platform
</h3>

<p align="left">
OCR • Document AI • Layout Understanding • LLM Integration • Distributed Systems
</p>

<p align="left">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Transformers](https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-000000?style=for-the-badge&logo=apachekafka&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-FF6B6B?style=for-the-badge)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=FF9900)

</p>

---

# Overview

DocIntell is a production-oriented Document Intelligence platform capable of understanding, processing and analyzing structured as well as unstructured documents.

Instead of treating documents as plain text, DocIntell combines OCR, layout-aware transformers, semantic embeddings and Large Language Models to extract meaningful information and enable intelligent document interactions.

The project is designed around scalable backend architecture and distributed processing, making it suitable for high-volume enterprise document workflows.

---

# Features

### Document Processing

- PDF/Image Upload
- Automatic File Conversion
- OCR Pipeline
- Layout-aware Document Understanding
- Multi-page Document Support

### AI Features

- Document Classification
- Key Information Extraction
- Layout-aware Embeddings
- Semantic Search
- Document Similarity Search
- LLM-powered Summarization
- Chat with Documents
- Metadata Extraction

### Backend Features

- REST API
- Asynchronous Processing
- Event-driven Architecture
- Microservice Ready
- Dockerized Deployment

---
```mermaid
flowchart TB

    Client["👤 Client / Frontend"]

    Gateway["🚪 API Gateway"]

    Upload["📤 Upload Service"]
    Search["🔍 Search Service"]
    AI["🤖 AI Service"]

    Converter["📄 Converter Service"]
    OCR["📝 OCR Service"]
    Layout["📐 Layout Service"]
    LM["🧠 LayoutLMv3"]
    Embed["🔗 Embedding Service"]

    Kafka["📨 Kafka Event Bus"]

    Redis["⚡ Redis Cache"]
    PG["🗄️ PostgreSQL"]
    Qdrant["📚 Qdrant Vector DB"]

    LLM["💬 LLM Provider"]

    Client --> Gateway

    Gateway --> Upload
    Gateway --> Search
    Gateway --> AI

    Upload --> Converter
    Converter --> OCR
    OCR --> Layout
    Layout --> LM
    LM --> Embed

    Embed --> PG
    Embed --> Redis
    Embed --> Qdrant

    Embed --> Kafka

    AI --> LLM
```
---

# Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn

## AI / Machine Learning

- EasyOCR
- LayoutLMv3
- HuggingFace Transformers
- PyTorch

## Data

- PostgreSQL
- Redis
- Qdrant Vector Database

## Distributed Systems

- Apache Kafka
- Docker
- Docker Compose

---
```mermaid
flowchart LR

    Upload["📄 Upload Document"]

    Convert["Convert to Images"]

    OCR["OCR"]

    Layout["Bounding Boxes"]

    LM["LayoutLMv3"]

    Embed["Document Embeddings"]

    Classify["Classification"]

    Extract["Field Extraction"]

    Search["Semantic Search"]

    Summary["LLM Summary"]

    Upload --> Convert
    Convert --> OCR
    OCR --> Layout
    Layout --> LM
    LM --> Embed

    Embed --> Classify
    Embed --> Extract
    Embed --> Search
    Embed --> Summary
```

```mermaid
mindmap
  root((DocIntell))

    Document Processing
      PDF Upload
      Image Upload
      OCR
      Multi-page Support

    Document AI
      LayoutLMv3
      Classification
      Embeddings
      Key Information Extraction

    Search
      Semantic Search
      Similar Documents
      Vector Database

    LLM
      Summarization
      Chat with Documents
      Question Answering

    Backend
      FastAPI
      Docker
      Kafka
      Redis
      PostgreSQL

    Deployment
      AWS
      Microservices
      CI/CD
```

# Future Roadmap

- OCR Pipeline Optimization
- Document Versioning
- Distributed Worker Services
- Kafka Event Streaming
- Vector Search
- Multi-document Chat
- Knowledge Graph Generation
- Role Based Authentication
- Real-time Processing Dashboard
- Kubernetes Deployment
- CI/CD Pipeline
- ML Model Registry

---
