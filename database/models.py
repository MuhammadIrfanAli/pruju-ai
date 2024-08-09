from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from rag_service.retrievers.enums import RetrieverType
from rag_service.generators.enums import GeneratorType

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class RAGConfig(Base):
    __tablename__ = "rag_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    rag_name = Column(String, index=True)
    rag_id = Column(String, unique=True, index=True)
    retriever_name = Column(String, unique=True, index=True)
    retriever_type = Column(Enum(RetrieverType))
    generator_type = Column(Enum(GeneratorType))
    generator_key = Column(String)

