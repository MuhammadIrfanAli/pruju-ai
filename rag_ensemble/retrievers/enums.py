import enum


# Define an enumeration for retriever type
class RetrieverType(enum.Enum):
    FAISS = "faiss"
    QDRANT = "qdrant"