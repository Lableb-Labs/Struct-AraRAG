from normalization import arabic_normalization
import pandas as pd
from pathlib import Path

import re

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# FULL PREPROCESSING PIPELINE
# ==========================================================

def preprocess_ebook_corpus(input_path, output_path):

    df = pd.read_excel(input_path)

    # ------------------------------------------------------
    # COLUMN GROUPS
    # ------------------------------------------------------

    english_lower_cols = [
        "category",
        "category.main",
        "origlang",
        "origauthor",
        "origtitle"
    ]

    arabic_cols = [
        "author",
        "title",
        "text",
        "origlang.ar"
    ]

    # ------------------------------------------------------
    # ENGLISH NORMALIZATION (LOWERCASE ONLY)
    # ------------------------------------------------------

    for col in english_lower_cols:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: str(x).lower().strip() if not pd.isna(x) else x
            )

    # ------------------------------------------------------
    # ARABIC NORMALIZATION PIPELINE
    # ------------------------------------------------------

    def clean_arabic_text(text):

        if pd.isna(text):
            return text

        text = str(text)

        # remove special chars
        text = re.sub(r"[^\u0600-\u06FFa-zA-Z0-9\s]", " ", text)

        # remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        # normalize arabic
        text = arabic_normalization(text)

        return text

    for col in arabic_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_arabic_text)

    # ------------------------------------------------------
    # SAVE OUTPUT
    # ------------------------------------------------------

    output_file = output_path

    df.to_excel(output_file, index=False)

    print(f"[DONE] Saved cleaned file → {output_file}")




input_file = BASE_DIR / "dataset" / "The_Arabic_E-Book_Corpus.xlsx"
output_file = BASE_DIR / "dataset" / "The_Arabic_E-Book_Corpus_v2.xlsx"
preprocess_ebook_corpus(input_file, output_file)