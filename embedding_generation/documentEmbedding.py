import json
from pathlib import Path

from embedding_generation.queryEmbedding import get_embedding
BASE_DIR = Path(__file__).resolve().parent.parent

input_file_name = "books_for_vectordb_v2.json"
output_file_name = "books_vectors_v2.json"
input_file = BASE_DIR / "embedded_data" / input_file_name
output_file = BASE_DIR / "embedded_data" / output_file_name

# =========================
# LOAD CLEAN BOOKS
# =========================
with open(input_file, "r", encoding="utf-8") as f:
    books = json.load(f)

# =========================
# GENERATE EMBEDDINGS
# =========================
content_data = []

for i, book in enumerate(books):
    print(i)
    book_id = book["id"]
    content = book["text"]
    # --------------------------------
    # CONTENT EMBEDDING
    # --------------------------------

    content_emb = get_embedding(content)

    content_data.append({
        "id": book_id,
        "content": content,
        "content_emb": list(content_emb)
    })


# =========================
# SAVE JSON FILES
# =========================
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(content_data, f, ensure_ascii=False)

print("Embeddings generated and saved successfully.")