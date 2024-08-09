from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import RAGConfig
from rag_service.retrievers.enums import RetrieverType
from rag_service.generators.enums import GeneratorType
from pydantic import BaseModel
from typing import List
import os
from fastapi.responses import FileResponse

from fastapi import FastAPI, Query
from typing import List
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
import json

def load_list_from_json(file_path):
    """
    Load a list of strings from a JSON file.
    
    :param file_path: Path to the JSON file to be read.
    :return: List of strings loaded from the JSON file.
    """
    with open(file_path, 'r') as file:
        strings_list = json.load(file)
    return strings_list


router = APIRouter()


# Pydantic model for creating and updating RAG configs
class RAGConfigCreate(BaseModel):
    rag_name: str
    rag_id: str
    retriever_name: str
    retriever_type: RetrieverType
    generator_type: GeneratorType
    generator_key: str

class RAGConfigUpdate(BaseModel):
    rag_name: str
    retriever_name: str
    retriever_type: RetrieverType
    generator_type: RetrieverType
    generator_key: str

def list_files_in_directory(directory, exclude_files=None, exclude_extensions=None):
    if exclude_files is None:
        exclude_files = ['.DS_Store']
    if exclude_extensions is None:
        exclude_extensions = ['.html', '.docx', 'odt']
    
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename in exclude_files or any(filename.endswith(ext) for ext in exclude_extensions):
                continue
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

@router.post("/rag/", response_model=RAGConfigCreate)
def create_rag_config(rag_config: RAGConfigCreate, db: Session = Depends(get_db)):
    db_rag_config = RAGConfig(**rag_config.dict())
    db.add(db_rag_config)
    db.commit()
    db.refresh(db_rag_config)
    return db_rag_config

@router.put("/rag/{rag_id}", response_model=RAGConfigUpdate)
def update_rag_config(rag_id: str, rag_config: RAGConfigUpdate, db: Session = Depends(get_db)):
    db_rag_config = db.query(RAGConfig).filter(RAGConfig.rag_id == rag_id).first()
    if db_rag_config is None:
        raise HTTPException(status_code=404, detail="RAGConfig not found")
    for key, value in rag_config.dict().items():
        setattr(db_rag_config, key, value)
    db.commit()
    db.refresh(db_rag_config)
    return db_rag_config

@router.delete("/rag/{rag_id}", response_model=dict)
def delete_rag_config(rag_id: str, db: Session = Depends(get_db)):
    db_rag_config = db.query(RAGConfig).filter(RAGConfig.rag_id == rag_id).first()
    if db_rag_config is None:
        raise HTTPException(status_code=404, detail="RAGConfig not found")
    db.delete(db_rag_config)
    db.commit()
    return {"detail": "RAGConfig deleted"}

@router.get("/rag/{rag_id}", response_model=RAGConfigCreate)
def read_rag_config(rag_id: str, db: Session = Depends(get_db)):
    db_rag_config = db.query(RAGConfig).filter(RAGConfig.rag_id == rag_id).first()
    if db_rag_config is None:
        raise HTTPException(status_code=404, detail="RAGConfig not found")
    return db_rag_config

@router.get("/rag/", response_model=List[RAGConfigCreate])
def list_rag_configs(db: Session = Depends(get_db)):
    rag_configs = db.query(RAGConfig).all()
    return rag_configs

@router.get("/rag/{rag_id}/ivfflat1.index")
def list_rag_configs(rag_id: str):
    file_path = os.path.join('course_material_vdb', 'ivfflat_index.index')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

index_filename = 'ivfflat_index.index'
index = faiss.read_index(index_filename)
model = SentenceTransformer('all-MiniLM-L6-v2')  # Use the same model as used for encoding
# vector_store = FAISS(index)
# vector_store = FAISS.load_local(
#     "course_material_vdb/updated", HuggingFaceInstructEmbeddings(cache_folder=os.getenv("MODEL_CACHE"), model_name="sentence-transformers/all-MiniLM-L6-v2"))

@router.get("/rag/{rag_id}/chunks/")
def chunks():
    # Encode the query to get the query vector
    documents = load_list_from_json('document_index.json')
    return {"documents": documents}

@router.get("/rag/{rag_id}/search/")
def search(query: str, top_k: int = 5):
    # Encode the query to get the query vector
    mock_query =' What are the basic techniques in text analytic?'
    query_vector = model.encode([query], convert_to_tensor=False)
    query_vector = np.array(query_vector).astype('float32')

    query_vector = model.encode([query], convert_to_tensor=False).astype('float32')
    # D, I = index.search(query_vector, top_k)

    return {"query": query, "query_vector": query_vector[0].tolist()}

@router.get("/rag/{rag_id}/files")
def list_rag_configs(db: Session = Depends(get_db)):
    try:
        files = list_files_in_directory('course_material')
        return {"files": files}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")

@router.post("/rag/{rag_id}/chat", response_model=RAGConfigCreate)
def read_rag_config(rag_id: str, db: Session = Depends(get_db)):
    db_rag_config = db.query(RAGConfig).filter(RAGConfig.rag_id == rag_id).first()
    if db_rag_config is None:
        raise HTTPException(status_code=404, detail="RAGConfig not found")
    return db_rag_config

@router.post("/rag/{rag_id}/upload", response_model=RAGConfigCreate)
def read_rag_config(rag_id: str, db: Session = Depends(get_db)):
    db_rag_config = db.query(RAGConfig).filter(RAGConfig.rag_id == rag_id).first()
    if db_rag_config is None:
        raise HTTPException(status_code=404, detail="RAGConfig not found")
    return db_rag_config