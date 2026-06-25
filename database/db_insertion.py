import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from pathlib import Path

from database.config import DB_CONFIG

BASE_DIR = Path(__file__).resolve().parent.parent


embedded_dir = BASE_DIR / "embedded_data"
embedded_dir.mkdir(parents=True, exist_ok=True)

input_file = BASE_DIR / "dataset" / "The_Arabic_E-Book_Corpus_v2.xlsx"
output_file = BASE_DIR /"embedded_data"/ "books_for_vector_db_v2.json"

table_name = "books_v2"


def clean_value(v):
    if pd.isna(v):
        return None
    return v


def ingest_books():

    conn = psycopg2.connect(**DB_CONFIG)

    cur = conn.cursor()

    # --------------------------------------------------
    # READ EXCEL
    # --------------------------------------------------

    df = pd.read_excel(
        input_file
    )


    # --------------------------------------------------
    # JSON FOR VECTOR DB
    # --------------------------------------------------

    vector_documents = []

    # --------------------------------------------------
    # INSERT DATA
    # --------------------------------------------------

    insert_rows = []

    for _, row in df.iterrows():

        booknr = clean_value(row.get("booknr"))

        if booknr is None:
            continue

        # ------------------------------------------
        # DATABASE ROW
        # ------------------------------------------

        insert_rows.append(

            (
                int(booknr),

                clean_value(row.get("category")),

                clean_value(row.get("author")),

                clean_value(row.get("pubdate")),

                clean_value(row.get("origtitle")),

                clean_value(row.get("origauthor")),

                clean_value(row.get("wc")),

                clean_value(row.get("origpubdate")),

                clean_value(row.get("origlang.ar")),

                clean_value(row.get("transdate")),

                clean_value(row.get("translation")),

                clean_value(row.get("origlang")),

                clean_value(row.get("origpubdate.full")),

                clean_value(row.get("transdate.full")),

                clean_value(row.get("category.main"))
            )
        )

        # ------------------------------------------
        # VECTOR DB JSON
        # ------------------------------------------

        vector_documents.append(
            {
                "id": int(booknr),
                "title": clean_value(row.get("title")),
                "text": clean_value(row.get("text"))
            }
        )

    # --------------------------------------------------
    # BULK INSERT
    # --------------------------------------------------

    sql = f"""
    INSERT INTO {table_name}
    (
        booknr,
        category,
        author,
        pubdate,
        origtitle,
        origauthor,
        wc,
        origpubdate,
        origlang_ar,
        transdate,
        translation,
        origlang,
        origpubdate_full,
        transdate_full,
        category_main
    )
    VALUES
    (
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s
    )
    ON CONFLICT (booknr)
    DO NOTHING
    """

    execute_batch(
        cur,
        sql,
        insert_rows,
        page_size=1000
    )

    conn.commit()

    print(
        f"Inserted {len(insert_rows)} books into PostgreSQL"
    )

    # --------------------------------------------------
    # SAVE JSON FOR VECTOR DB
    # --------------------------------------------------

    with open(
            output_file,
        "w",
        encoding="utf-8"
    ) as outfile:

        json.dump(
            vector_documents,
            outfile,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"Saved {len(vector_documents)} vector documents"
    )

    cur.close()
    conn.close()


ingest_books()