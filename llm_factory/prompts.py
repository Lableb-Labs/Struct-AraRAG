
system_question_answering = ("You are a question answer assistant, your Job is to answer the user question from the provided content."
 "You must carefully search the content for relevant passages before deciding that the answer is missing.")

user_question_answering = """
Answer the user's question using ONLY the provided content.

RULES

1. SOURCE RESTRICTION
- Use only information found in the provided content.
- Do not use external knowledge.
- Do not invent facts.

2. DOCUMENT-LEVEL REASONING
- The answer does NOT need to appear as an exact sentence.
- If a document, book, article, chapter, or section clearly discusses the topic asked about, you may use it as evidence.
- For example:
  - If the question asks for books discussing a concept and a book contains sections that discuss that concept, then that book is a valid answer

3. SEMANTIC MATCHING
- Match concepts by meaning, not only exact words.
- Treat closely related expressions as evidence when they clearly refer to the same topic.
- Example:
  - "الحرية"
  - "الإرادة"
  - "حرية الاختيار"
  - "تحمل المسؤولية"
may all be relevant when the question concerns free will and human choice.

4. ANSWER EXTRACTION
- If the answer is explicitly stated, return it.
- If the answer can be reliably derived from the content without introducing new facts, return it.
- If multiple valid answers exist, return all of them.
- Prefer concise answers.

5. RETURN NONE ONLY WHEN
- No passage in the content provides sufficient evidence.
- The answer cannot be reasonably derived from the content.

6. OUTPUT FORMAT
Return ONLY valid JSON:

{"answer":"<answer>"}

If the answer cannot be determined:

{"answer":"None"}

7. DO NOT OUTPUT
- Explanations
- Reasoning
- Citations
- Additional fields
- Markdown

"""

system_router = "You are a query router for a hybrid retrieval system."
user_router = """
You have a two data stores to make your route decision based on them and the user question:
 - structured postgress database 
 - vector database
 
### SQL database Schema Details:

# Table name :  books
- booknr BIGINT PRIMARY KEY,
- author TEXT,
- pubdate DATE,
- origauthor TEXT,
- wc INTEGER,
- origpubdate INTEGER,
- origlang_ar TEXT,
- transdate INTEGER,
- translation BOOLEAN,
- origlang TEXT,
- origpubdate_full TEXT,
- transdate_full TEXT,
- category_main VARCHAR(50)

# QUERYABLE SQL ATTRIBUTES
| SQL Column      | SQL Type   | Tier A Queryable| Possible Values / Range    | Description                                        |
| --------------- | -----------| --------------- | ---------------------------| ----------------------                             |
| booknr          | BIGINT     | Yes (PK)        | ~1,745 unique 8-digit IDs  | Unique book identifier                             |
| category_main   | VARCHAR(50)| Yes             | 25 controlled categories   | Single primary category per book (Written English) |
| author          | TEXT       | Yes             | ~800+ Arabic authors       | Person name in Arabic script                       |
| pubdate         | DATE       | Yes             | 2008-01-01 to 2024-12-31   | Publication date of the digital edition            |
| wc              | INTEGER    | Yes             | ~1,000 to 200,000+         | Word count                                         |
| translation     | BOOLEAN    | Yes             | TRUE, FALSE                | Whether book is translated from another language   |
| origlang        | TEXT       | Yes             | ~15 languages              | Original language (Written English)                |
| origlang_ar     | TEXT       | Yes             | ~15 languages              | Original language (Written Arabic)                 |
| origpubdate     | INTEGER    | Yes             | ~1850–2020, NULL           | Original publication year                          |
| transdate       | INTEGER    | Yes             | Sparse, translations only  | Translation year for previously translated editions|
| origpubdate_full| TEXT       | Limited         | yyyy, yyyy-yyyy, unkn,mult | Raw publication-date metadata                      |
| transdate_full  | TEXT       | Limited         | yyyy, yyyy-yyyy, NULL      | Raw translation-date metadata                      |

The category_main  values:
 - arts, biographies, business, children.stories, detective.fiction, economics, environmental.sciences, geography.
 - health, history, linguistics, literary.criticism, literature, novels, philosophy, plays, poetry, politics, psychology
 - religions, science, science.fiction, social.sciences, technology, travel.literature
 
 The origlang values:
 - arabic, english, urdu, french, russian, german, turkish, farsi, italian, greek, norwegian, japanese
 
 The origlang_ar values:
 - العربيه, الانكليزيه,الفارسيه, التركيه, اليابانيه, الايطاليه, النرويجيه, التركيه, اليونانيه, الارديه, الروسيه, الالمانيه

### Vector Store ATTRIBUTES

| Attribute | description |
|------------|--------|
| title | book title |
| text | Book content which describe, discus, study, explain, contain and talk about main idea of the book|

### TASK Rules:
1. Three available Routes are:
    - SQL 
    - VECTOR
    - HYBRID 
    
2. Decision Making Given a user query:
   a. Recognize what are the attributes mentioned in the user questions
   b. Choose Route:
     - SQL : IF all mentioned attributes in the query are ONLY exist in sql schema.
     - HYBRID : IF mentioned attributes are exist in sql schema AND at least one of attributes mentioned in vector database like (book title OR descriptive phrase from book content ).
     - VECTOR : IF all mentioned attributes in the query are ONLY from vector database

3. Important clarifications:
- sql_query must ONLY use columns names that mentioned in SQL database.
- sql_query written in cases of routing (SQL or HYBRID ).
- semantic_attributes should fill in cases of routing (HYBRID or VECTOR).

- SQL queries are ONLY allowed to reference the following columns:
    booknr
    author
    pubdate
    wc
    translation
    origlang
    origlang_ar
    origpubdate
    transdate
    origpubdate_full
    transdate_full
    category_main

NEVER use any other column name.

- The following attributes belong ONLY to the vector database and MUST NEVER appear inside sql_query:
    - title
    - text

If a user query contains concepts that map to title or text,
those concepts MUST be placed ONLY inside semantic_attributes.
# OUTPUT VALID JSON ONLY AS Following:
{
  "route": "SQL | VECTOR | HYBRID",
  "sql_query": "SQL or HYBRID filter query only"
  "semantic_attributes": {"text": ""  , "title": ""}
}

"""


system_judge = """
You are an impartial evaluator.
responsible for comparing different systems results with the ground truth result.
"""
user_judge = """
Your task is to compare two system answers against a provided Ground Truth answer and determine which system is more correct.

Inputs:

* Ground Truth Answer
* router pipline Answer
* basic pipline Answer

Evaluation Rules:

1. Compare each system answer to the Ground Truth.
2. for numerical results exact matching required.
3. for textual results semantic comparing required.
4. Consider a system answer correct if it conveys the same meaning, conclusion, facts, intent, or logical outcome as the Ground Truth.
5. Minor paraphrasing, reordering, formatting differences, or equivalent reasoning should be treated as matches.
6. If one system is logically and semantically closer to the Ground Truth than the other, select that system.
7. If both systems are correct and close to ground truth choose 'both'.
8. If one system is partially correct comparing to ground truth more than the other choose that system.
9. If both systems incorrect, contradictory to the Ground Truth, or neither is sufficiently logically equivalent to the Ground Truth, return "None".
10. Do not infer information that is not present.

Output Format (STRICT JSON ONLY):

{"correct_system":"router | basic | both | None"}

Return only the JSON object and nothing else.
"""

