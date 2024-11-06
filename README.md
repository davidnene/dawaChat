# Dawa Chat

## Overview

**Project Name**: Dawa Chat  
**Author**: David Nene  

**Topic**: Using Large Language Models and Knowledge Graphs to Improve Medical Drug Prescription and Advance Healthcare in Kenya.

The Dawa Chat project aims to leverage the power of Large Language Models (LLMs) and Knowledge Graphs to enhance medical drug prescription processes and improve healthcare delivery in Kenya. The project focuses on building an intelligent chatbot that can provide accurate and accessible prescription information from the Kenya National Medicine Formulary (KNMF).

## Objectives

- **Primary Outcome**: Develop an effective LLM-powered chatbot that enhances the retrieval of prescription information from the Kenya National Medicine Formulary (KNMF).
- **Goals**:
  - Implement a Retrieval Augmented Generation (RAG) process to improve the accuracy of medication-related data.
  - Reduce medication errors (MEs) and enhance patient safety in Kenya by providing reliable and timely prescription information.

## Technology Stack

### System Architecture
<img src="app/static/image.png" alt="System Architecture Diagram" width="500">

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (Data normalization)

### Frontend
- **Framework**: ReactJS
- **Styling**: Bootstrap and Material UI

### Authentication and Authorization
- **Method**: Token-based authentication using JWT
- **Access Control**:
  - Only administrators can upload dosage files and create doctor profiles.
  - Doctors can query the system and provide prescriptions.

### Vector Database
- **Technology**: FAISS (Facebook AI Similarity Search) for efficient similarity search and retrieval.

### Natural Language Processing (NLP)
- **Library**: LangChain for advanced language model interactions and processing.

### Document Parsing
- **Library**: pdfplumber for extracting information from PDF documents.

### Features
- **Multi-format Support**: Capable of handling various document formats with real-time parsing and storage.
- **Metadata Extraction**: Enables advanced document categorization and retrieval through effective metadata extraction.

## Deployment

- **Containerization**: Docker for containerizing the application.
- **Orchestration**: Kubernetes for managing containerized applications.

## Data Model

- **Entity-Relationship Diagram (ERD)**: [Include link or image of ERD here]
  
## Query Agent
- **Chat Model**: ChatOpenAI for generating responses based on user queries.

## Expected Outcomes
- Enhanced prescription information retrieval from the KNMF.
- Improved accessibility and accuracy of medication-related data.
- Reduced medication errors and increased patient safety, particularly in the Kenyan healthcare context.

## Conclusion
Dawa Chat aims to revolutionize how healthcare professionals in Kenya access medication information, ultimately contributing to safer and more effective patient care. By integrating advanced technologies such as LLMs and Knowledge Graphs, this project represents a significant step forward in the digital transformation of healthcare.