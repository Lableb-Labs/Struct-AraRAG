import json

import pandas as pd
from database.db_engine import PostgresDB
from database.postprocessing import format_sql_result
from retrievers.dataIndexing import (
    searcher_content
)
from llm_factory.LLMSpecialists import LLMSpecialists


class HybridRetrieverSystem:

    def __init__(self):

        self.db = PostgresDB()

        self.content_searcher = searcher_content

    # =====================================================
    # MAIN PIPELINE
    # =====================================================
    def process_query(self, user_query):

        router_output = LLMSpecialists().router(user_query)
        print("router_output : ", router_output)
        route = router_output["route"]


        if route == "SQL":
            return self.handle_sql(router_output)

        elif route == "VECTOR":
            return self.handle_vector(router_output)

        elif route == "HYBRID":
            return self.handle_hybrid(router_output)

        return {"error": "Unknown route" }

    # =====================================================
    # SQL ROUTE
    # =====================================================
    def handle_sql(self, router_output):

        sql_query = router_output.get("sql_query")
        # print("sql_query :", sql_query)
        if not sql_query:
            return {
                "route": "SQL",
                "error": "No SQL query generated"}

        try:
            results = self.db.execute_query(sql_query)
            formatted_results = format_sql_result(results)
            # print("formatted_results sql : " ,formatted_results)
            return {
                "route": "SQL",
                "sql_query": sql_query,
                "results": formatted_results
            }

        except Exception as e:
            return {
                "route": "SQL",
                "error": str(e)
            }


    # =====================================================
    # VECTOR ROUTE
    # =====================================================
    def handle_vector(self, router_output):

        semantic_attributes = router_output["semantic_attributes"]

        final_results = []
        # -----------------------------------------
        # CONTENT SEARCH
        # -----------------------------------------
        content_query_parts = []

        if semantic_attributes.get("title"):
            content_query_parts.append(
                semantic_attributes["title"]
            )

        if semantic_attributes.get("text"):
            content_query_parts.append(
                semantic_attributes["text"]
            )

        if len(content_query_parts) > 0:

            content_query = " ".join(content_query_parts)


            final_results = self.content_searcher.search(
                query=content_query,
                k=3
            )


        return {
            "route": "VECTOR",
            "semantic_attributes": semantic_attributes,
            "results": final_results
        }

    # =====================================================
    # HYBRID ROUTE
    # =====================================================
    def handle_hybrid(self, router_output):

        # =========================================
        # STEP 1 -> SQL FILTERING
        # =========================================
        sql_query = router_output.get("sql_query")
        # print("sql_query :", sql_query)

        sql_results = self.db.execute_query(
            sql_query
        )

        allowed_ids = [
            row[0]
            for row in sql_results
        ]


        if len(allowed_ids) == 0:
            return {
                "route": "HYBRID",
                "sql_query": sql_query,
                "semantic_attributes": router_output.get("semantic_attributes"),
                "results": []
            }

        # =========================================
        # STEP 2 -> SEMANTIC SEARCH
        # ONLY INSIDE SQL IDS
        # =========================================
        semantic = router_output[
            "semantic_attributes"
        ]

        final_results = []

        # -----------------------------------------
        # CONTENT SEARCH
        # -----------------------------------------
        content_query_parts = []

        if semantic.get("title"):
            content_query_parts.append(
                semantic["title"]
            )

        if semantic.get("text"):
            content_query_parts.append(
                semantic["text"]
            )
        if len(content_query_parts) > 0:
            content_query = " ".join(
                content_query_parts
            )

            final_results = (
                self.content_searcher.search(
                    query=content_query,
                    allowed_ids=allowed_ids,
                    k=3
                )
            )

        return {
            "route": "HYBRID",
            "sql_query": sql_query,
            "semantic_attributes": router_output.get("semantic_attributes"),
            "results": final_results
        }



