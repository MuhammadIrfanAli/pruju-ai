def get_vector_store(store_path, store_type, store_id, store_name):
    if store_type == STORE_FAISS:
        return FaissVectorStore(store_id, store_name)