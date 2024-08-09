from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Body,  File, UploadFile
from fastapi.responses import JSONResponse
from read_to_vectorstore import add_files_to_vector_store
from fastapi import APIRouter

from chat_caller import query_gpt_chat, reload_vector_store
import os
import uvicorn

router = APIRouter()

# Directory path to store uploaded files
UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploads")

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    print("Received File: ", file.filename)
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    add_files_to_vector_store(UPLOAD_DIRECTORY, 'prujuai_resources/faiss_index')
    reload_vector_store()
    
    return JSONResponse(content={"filename": file.filename, "message": "File uploaded successfully"})


@router.post("/chat")
async def chat_endpoint(query: dict = Body(...)):
    
    messages = query['messages']
    message = messages[-1]["content"]
    content =  query_gpt_chat(
        message,
        [msg["content"] for msg in query['messages'][:]],
        is_api=True
    )[1]

    return  {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"PRUJU AI: {content}"
                },
            }
        ],
    }
    