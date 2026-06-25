# Struct-AraRAG

## Overview

This repository contains the implementation and experimental pipeline used in the research paper **[Struct-AraRAG]**. The system processes an Arabic eBook corpus, stores structured metadata in a PostgreSQL database, generates embeddings for unstructured text, and executes the complete retrieval pipeline.

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

---

## AraAggBench: Test Set for Evaluation

To evaluate the proposed **Arabic Structure-RAG framework**, we introduce **AraAggBench**, a benchmark designed for **aggregative question answering over mixed structured and unstructured Arabic data sources**.

### Dataset Overview

AraAggBench consists of **100 evaluation questions**, carefully stratified based on the type of retrieval strategy required to answer them. The dataset is designed to test different levels of reasoning across structured databases and unstructured textual corpora.

**Dataset Path:**

```text
dataset/AraAggBench_100_Questions_TestSet.csv
```

---

### Question Stratification (Tiers)

The dataset is divided into three tiers:

* **Tier A — Pure SQL (40 questions)**
  Questions that require only structured retrieval and aggregation over relational data.

* **Tier B — Hybrid SQL + Vector (40 questions)**
  Questions requiring both structured filtering (SQL) and semantic retrieval from unstructured text (vector search).

* **Tier C — Pure Vector (20 questions)**
  Questions answered solely through semantic retrieval over unstructured text, without reliance on structured metadata.

---

### Dataset Fields

Each entry in AraAggBench contains the following fields:

* **Tier**
  Indicates the retrieval category (A, B, or C).

* **Question_Arabic**
  The original question written in Arabic.

* **Question_English**
  English translation of the question.

* **Difficulty**
  Difficulty level assigned to the question: *Easy, Medium, Hard*.

* **SQL_Query** *(optional)*
  SQL query provided for Tier A and Tier B questions where structured retrieval is required.

* **Documents_IDs** *(optional)*
  IDs of the retrieved documents in Tier B and Tier C questions where semantic retrieval is applied.

* **Final_Answer**
  Ground-truth answer used for evaluation.

---

### DataSet Fields Generation
The details of dataset Constructions provided in the paper.

### Data Validation

SQL queries included in the dataset were **manually reviewed and validated** to ensure correctness and consistency.

---

### Notes

* The dataset is designed specifically for evaluating **multi-source retrieval systems combining structured and unstructured data**.
* Tier distribution ensures balanced evaluation across retrieval paradigms.

---