import faiss
import numpy as np

from embedding_generation.queryEmbedding import get_embedding


class FaissSemanticSearcher:

    def __init__(self, data, embedding_key, text_key, dimension=384):

        self.data = data
        self.dimension = dimension

        self.embedding_key = embedding_key
        self.text_key = text_key

        self.ids = []
        self.texts = []
        self.embeddings = []

        self._prepare_data()

    # ==================================
    # PREPARE DATA
    # ==================================
    def _prepare_data(self):

        for d in self.data:

            self.ids.append(d["id"])

            self.texts.append(d[self.text_key])

            self.embeddings.append(d[self.embedding_key])

    # ==================================
    # SEARCH
    # ==================================
    def search(
            self,
            query,
            allowed_ids=None,
            threshold=0.7,
            k=10,
            gap=0.05
    ):

        # ==================================
        # BUILD FILTERED SUBSET
        # ==================================
        filtered_embeddings = []
        filtered_ids = []
        filtered_texts = []
        for i in range(len(self.ids)):

            db_id = self.ids[i]

            if allowed_ids is not None:

                if db_id not in allowed_ids:
                    continue

            filtered_embeddings.append(
                self.embeddings[i]
            )

            filtered_ids.append(
                self.ids[i]
            )

            filtered_texts.append(
                self.texts[i]
            )
        # ==================================
        # NO DATA
        # ==================================
        if len(filtered_embeddings) == 0:
            return []

        # ==================================
        # BUILD TEMP INDEX
        # ==================================
        temp_index = faiss.IndexFlatL2(
            self.dimension
        )

        temp_embeddings = np.array(
            filtered_embeddings
        ).astype("float32")

        temp_index.add(temp_embeddings)

        # ==================================
        # QUERY EMBEDDING
        # ==================================
        query_text = f"query: {query}"

        query_vector = np.array([
            get_embedding(query_text)
        ]).astype("float32")

        # ==================================
        # SEARCH
        # ==================================
        distances, indices = temp_index.search(
            query_vector,
            min(k, len(filtered_embeddings))
        )

        distances = distances[0]
        indices = indices[0]

        filtered_results = []

        for i in range(len(distances)):

            dist = distances[i]

            if dist <= threshold:

                filtered_results.append(
                    (indices[i], dist)
                )

        # ==================================
        # GAP SPLITTING
        # ==================================
        selected_indices = self._split_by_max_gap(
            filtered_results,
            gap
        )

        # ==================================
        # FORMAT RESULTS
        # ==================================
        results = []

        for idx in selected_indices:

            results.append({
                "id": filtered_ids[idx],
                "text": filtered_texts[idx]
            })

        return results

    # ==================================
    # GAP SPLITTING
    # ==================================
    def _split_by_max_gap(
            self,
            filtered_results,
            gap=0.03
    ):

        distances = []
        indices = []

        for ind, dist in filtered_results:

            distances.append(dist)
            indices.append(ind)

        split_index = len(distances)

        for i in range(1, len(distances)):

            diff = distances[i] - distances[i - 1]

            if diff > gap:

                split_index = i
                break

        return indices[:split_index]