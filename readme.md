# Struct-AraRAG: A Structured Relational and Vector Pipeline for Arabic Aggregative QA

## Overview

This repository contains the implementation and experimental pipeline used in the research paper **[Struct-AraRAG: A Structured Relational and Vector Pipeline for Arabic Aggregative QA]**. The system processes an Arabic eBook corpus, stores structured metadata in a PostgreSQL database, generates embeddings for unstructured text, and executes the complete retrieval pipeline.

---

## Prerequisites

### Python Version

* Python 3.11

### Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root directory and configure the following variables:

```env
LLM_URL=""
LLM_KEY=""

DATABASE_NAME="book_db"
DATABASE_USER="postgres"
DATABASE_PASSWORD=""
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
```

---

## Pipeline Setup

### Step 1: Download the Corpus

Download the dataset by running:

```bash
python data_preprocessing/download_corpus.py
```

---

### Step 2: Preprocess the Corpus

After downloading the dataset, preprocess the raw documents:

```bash
python data_preprocessing/arabic_ebook_preprocessing.py
```

This step performs data cleaning and preparation.

#### Output

* Structured attributes (e.g., `id`, `category`, `word_count`) are inserted into the PostgreSQL database.
* Unstructured fields ( `id`, `title`, `content`) are prepared for embedding generation.

---

### Step 3: Generate Document Embeddings

Generate embeddings for the unstructured textual data:

```bash
python embedding_generation/document_embedding.py
```

#### Output

Generated embeddings are stored in:

```text
embedded_data/
```

---

### Step 4: Run the Complete Pipeline

Once preprocessing and embedding generation are completed, execute the main application:

```bash
python main.py
```

This runs the complete retrieval and inference pipeline.

---

## Reproducibility

To reproduce the experimental environment:

1. Install Python 3.11.
2. Install dependencies from `requirements.txt`.
3. Configure the `.env` file.
4. Download the corpus.
5. Run preprocessing.
6. Generate embeddings.
7. Execute `main.py`.

Following these steps should reproduce the dataset preparation and retrieval pipeline used in the research paper.
