from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Body,  File, UploadFile
from fastapi.responses import JSONResponse
from read_to_vectorstore import add_files_to_vector_store

from chat_caller import query_gpt_chat, reload_vector_store
import os
import uvicorn

app_fastapi = FastAPI()

# Directory path to store uploaded files
UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploads")

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app_fastapi.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    print("Received File: ", file.filename)
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    add_files_to_vector_store(UPLOAD_DIRECTORY, 'prujuai_resources/faiss_index')
    reload_vector_store()
    
    return JSONResponse(content={"filename": file.filename, "message": "File uploaded successfully"})


@app_fastapi.post("/chat")
async def chat_endpoint(query: dict = Body(...)):
    
    messages = query['messages']
    message = messages[len(messages) - 1]["content"]
    content =  query_gpt_chat(
        message,
        [msg["content"] for msg in query['messages'][:]],
        is_api=True
    )[1]

    print("Content", content)
    return  {
        "id": "chatcmpl-9ZLqvFsD54kds0X0TID3PEmHWArwl",
        "object": "chat.completion",
        "created": 1718212509,
        "model": "gpt-4o-2024-05-13",
        "choices": [
            {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": f"PRUJU AI: {content}"
            },
            "logprobs": None,
            "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 19,
            "completion_tokens": 10,
            "total_tokens": 29
        },
        "system_fingerprint": "fp_319be4768e"
    }

if __name__ == "__main__":
    print("Launching Demo\n")
    isDocker = os.path.exists("/.dockerenv")
    choose_model(check_quota_status())
    # choose_model(check_quota_status())
    uvicorn.run(app_fastapi, host="0.0.0.0" if isDocker else "127.0.0.1", port=6500)
    