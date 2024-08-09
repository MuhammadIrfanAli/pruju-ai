import argparse
import os
import textract
import pandas as pd
import os 
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

def read_filenames_from_directory(material_directory: str):
    filenames = []
    for root, dirs, files in os.walk(material_directory):
        for name in files:
            # Exclude dot-files
            if name[0] != '.':
                filenames.append(os.path.join(root, name))
    return filenames

def create_material_headings_from_filenames(filenames, material_directory):
    # Make headings pretty based on file names
    # '_' to ' ', remove file suffixes, title case, "/" to ": " 
    material_headings = [filename[len(material_directory):] for filename in filenames]
    def pretty_headings(heading):
        heading = heading.replace('_', ' ')
        heading = heading.split('.')[0]
        heading = heading.title()
        heading = heading.replace('/', ': ') 
        return heading
    material_headings = [pretty_headings(heading) for heading in material_headings]
    return material_headings

def convert_files_totext(filenames):
    # Extract text from the files
    # Supported file formats: https://textract.readthedocs.io/en/stable/ + MarkDown
    texts = []
    for filename in filenames:
        # Exctract file type
        filetype = filename.split('.')[-1]
        print("Converting to text: " + filename)
        if filetype != "md":
            text = textract.process(filename)
            text = text.decode("utf-8")
        else:
            with open(filename) as f:
                text=f.read()
                f.close()

        texts.append(text)
    return texts

def create_chunck_dataframe(material_headings, texts):
    # Create data frame
    df = pd.DataFrame({'Heading': material_headings, 'Text': texts})

    # Create chunks
    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(        
        separator = "\n\n",
        chunk_size = 500,
        chunk_overlap  = 100,
        length_function = len,
        is_separator_regex = False,
    )
    df['Text_Splitted'] = df['Text'].apply(text_splitter.split_text)
    # Append Heading to the top of chunk
    df['Text_Splitted_w_Headings'] = df.apply(lambda row: ["Source: " + row['Heading'] + '\n' + chunk for chunk in row['Text_Splitted']], axis=1)
    return df

def create_vector_store(df,
                        store_type="faiss",
                        metadatas=False,
                        vector_store_endpoint=None,
                        vector_store_api_key=None,
                        vector_store_collection_name=None):
    master_chunk = []
    master_metadata=[]
    for i, row in df.iterrows():
        master_chunk += row['Text_Splitted_w_Headings']
        if metadatas:
            for text_in_row in row['Text_Splitted_w_Headings']:
                master_metadata.append(row[['Heading','Modified']].to_dict())
    # Create vector store
    embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if store_type=="faiss":
        vector_store = FAISS.from_texts(texts=master_chunk, embedding=embeddings,metadatas=master_metadata if metadatas else None)
    elif store_type=="qdrant":
        from langchain.vectorstores import Qdrant
        vector_store = Qdrant.from_texts(
            texts=master_chunk,
            embedding=embeddings,
            metadatas=master_metadata if metadatas else None,
            url=vector_store_endpoint,
            prefer_grpc=True,
            api_key=vector_store_api_key,
            collection_name=vector_store_collection_name,
            force_recreate=True,
        )
    else:
        print("Unsupported vector store detected. Returning None.")
        return None
    return vector_store

def add_files_to_vector_store(file_directory, vector_store_dir, vector_store_type="faiss", metadatas=False, vector_store_endpoint=None, vector_store_api_key=None, vector_store_collection_name=None):
    if vector_store_type == "faiss":
        vector_store = FAISS.load_local(vector_store_dir, HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
        print(f"Number of vectors before adding new resources: {vector_store.index.ntotal}")
    elif vector_store_type == "qdrant":
        vector_store = Qdrant(
            url=vector_store_endpoint,
            prefer_grpc=True,
            api_key=vector_store_api_key,
            collection_name=vector_store_collection_name,
        )
        print(f"Number of vectors before adding new resources: {vector_store.count()}")
    else:
        print("Unsupported vector store type.")
        return

    filenames = read_filenames_from_directory(file_directory)
    material_headings = create_material_headings_from_filenames(filenames, file_directory)
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
    if vector_store_type == "faiss":
        if metadatas:
            vector_store.add_texts(master_chunk, metadatas=master_metadata)
        else:
            vector_store.add_texts(master_chunk)
        vector_store.save_local(vector_store_dir)
        print(f"Number of vectors after adding new resources: {vector_store.index.ntotal}")
    elif vector_store_type == "qdrant":
        vector_store.add_texts(master_chunk, embeddings, metadatas=master_metadata if metadatas else None)
        print(f"Number of vectors after adding new resources: {vector_store.count()}")

    print("New resources added to the vector store successfully.")



def main():

    # Scan files from the course_material directory (or alternative)
    material_directory=args.load_dir+"/"
    folder = args.save_dir+"/"
    use_defaults = args.use_defaults
    print("Running script with the following arguments:")
    print(f"Directory for the course materials: {material_directory}")
    print(f"Directory to save the vector store: {folder}")
    print(f"Run the script with sensible defaults: {use_defaults}")
    print("---")

    print("The following files will be processed:\n")
    if use_defaults:
        dir_input = material_directory
    else:
        dir_input = input(f"Default materials directory: {material_directory}\nPress enter to keep the same, or write the desired name to change: ")
    if dir_input != '':
        material_directory = dir_input
    
    filenames=read_filenames_from_directory(material_directory=material_directory)
    print(filenames)
    material_headings=create_material_headings_from_filenames(filenames,material_directory)
    # Loop through suggested material headings and ask the user if they want to change it
    for i, heading in enumerate(material_headings):
        # print(heading)
        if use_defaults:
            user_input=heading
        else:
            user_input = input(f"Suggested heading: {heading}\nPress enter to keep the same, or write the desired name to change:")
        if user_input != '':
            material_headings[i] = user_input
    print(material_headings)

    texts = convert_files_totext(filenames)    
    df = create_chunck_dataframe(material_headings, texts)
    vector_store = create_vector_store(df,store_type="faiss")

    # Try querying the vector store

    print("Test querying the vector store.")
    try:
        if use_defaults:
            query="Default query."
        else:
            query = input("Search the database: ")
        docs = vector_store.similarity_search(query)
        print("Results of test query: ")
        print(docs)
    except Exception as e:
        print(f"An error occurred when performing a query: {e}")
        exit(1)

    # Ask for the folder to save the database in
    
    if use_defaults:
        folder_figured_out = True
    else:
        folder_figured_out = False
    while folder_figured_out == False:
        folder = input(f"What folder would you like to save the database in? Default: {folder} \n")
        if folder == "":
            folder = args.save_dir
            folder_figured_out = True
        if not os.path.exists(folder):
            print(f"Folder {folder} does not exist. Do you want to create it?")
            create_folder = input("Y/n: ")
            if create_folder.lower() == "y":
                os.mkdir(folder)
                folder_figured_out = True
            elif create_folder.lower() == "":
                os.mkdir(folder)
                folder_figured_out = True

    print(f"Saving database in {folder}")

    # Save the vector store
    try:
        vector_store.save_local(folder)
        print("Save succcess!")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    # Load the vector store for testing
    print("Test querying the vector store (loaded from disk).")
    try:
        loaded_vector_store = FAISS.load_local(folder, HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
        # Try querying the vector store

        if use_defaults:
            query="Default query."
        else:
            query = input("Search the database: ")
        docs = loaded_vector_store.similarity_search(query)
        print(docs)
        print("Success!")
    except Exception as e:
        print(f"An error occurred while loading vector store from disk: {e}")
    
    return df
