import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_file_name = "books_vectors_v2.json"
input_file = BASE_DIR / "embedded_data" / input_file_name

with open(input_file, "r", encoding="utf-8") as f:
    content_data_e5_small = json.load(f)


