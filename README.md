# ChatBot - Retrieval-Augmented Generation (RAG) implemented

## Tools Used
- Document AI
    - Process pdf, csv text
- GCP Text Embedding 
    - Embedding texts to vectors
- Vector Search
    - vector search + Cloud Storage
- LLM (Gemini AI)
    - Generate response according to vector search and prompt
- DataBase
    - SQL-Database PostgreSQL
    - NoSQL-Database Cassandra

## Flow
---
![Architecture](https://github.com/lyoudr/AI_chatbot/blob/main/rag.png)

## Cloud Service
---
- Kubernetes
    - Service: aichatbot-service
        - I used a LoadBalancer service type, which assigns an external IP, allowing the application to be accessed directly via that IP.

## Asynchronous Task
---
- RabbitMQ
    - Use RabbitMQ to manage asynchronous background tasks, enabling concurrent task processing without interrupting or detaching from the current application.

## Logging

I implemented Python logging within middleware to capture request and response details, storing this information in a Cassandra database for security monitoring and request analysis.

## Impact

By implementing the Retrieval-Augmented Generation (RAG) technique, I improved the quality and accuracy of responses generated from large language models (LLMs). By retrieving relevant documents or data, RAG models generate more accurate and contextually relevant responses, reducing the chances of incorrect or nonsensical information. Additionally, RAG systems can dynamically update knowledge, quickly adapting to new information without retraining the entire model, making them more flexible and responsive to changes in the information landscape.


