
class FaissRetriever(AbstractVectorStore):
    def __init__(self, file_path, embed_model="sentence-transformers/all-MiniLM-L6-v2"):
        self.file_path = file_path
        self.embed_model = embed_model
        self.store = None
    
    def load(self):
        self.store = FAISS.load_local(
            self.file_path, 
            HuggingFaceInstructEmbeddings(model_name=self.embed_modal)
        )

    def add_document(self, file_path, file_name, metadatas=False):
        filenames = [file_name]
        material_headings = create_material_headings_from_filenames(filenames, file_path)
        texts = convert_files_totext(filenames)
        new_df = create_chunck_dataframe(material_headings, texts)

        master_chunk = []
        master_metadata = []
        for i, row in new_df.iterrows():
            master_chunk += row['Text_Splitted_w_Headings']
            if metadatas:
                for text_in_row in row['Text_Splitted_w_Headings']:
                    master_metadata.append(row[['Heading', 'Modified']].to_dict())

        embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        new_vectors = embeddings.embed_documents(master_chunk)
        if metadatas:
            self.store.add_texts(master_chunk, metadatas=master_metadata)
        else:
            self.store.add_texts(master_chunk)
        self.store.save_local(vector_store_dir)

    def add_vectors(self, vectors, metadata=None):
        self.vectors.extend(vectors)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([None] * len(vectors))

    def search(self, query, smart_search=False):
        if smart_search==True:
            system="""
            You are an AI that provides assistance in database search. 
            Please translate the user's query to a list of search keywords
            that will be helpful in retrieving documents from a database
            based on similarity.
            The language of the keywords should match the language of the documents: 
            """+doc_language+"""\n
            Answer with a list of keywords.
            """
            query=chat(
                [SystemMessage(content=system),
                    HumanMessage(content=query)]
            ).content
        docs = self.store.similarity_search(query)
        context = "\n---\n".join(doc.page_content for doc in docs)
        return context

    def remove_document(self, file_path):
        # Dummy implementation: not saving to file
        pass

