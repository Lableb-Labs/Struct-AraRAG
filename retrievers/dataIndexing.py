from retrievers.dataLoader import (
    content_data_e5_small
)
from retrievers.retrival import FaissSemanticSearcher

searcher_content = FaissSemanticSearcher(
    data=content_data_e5_small,
    embedding_key="content_emb",
    text_key="content"
)
