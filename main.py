import os,uuid
from fastapi import UploadFile,File,FastAPI
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
UPLOAD_DIR="storedmodels"
ALLOWED_EXTENSIONS={".gltf",".fbx",".glb",".blend"}
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.post("/api/models/upload")
async def upload_model(
    file: UploadFile=File(...)):
    file_ext=os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return{
            "success":False,
            "error":"Unsupported file type. Only GLTF/FBX/Blender files are allowed."
        }
    model_Id=uuid.uuid4().hex[:8]
    unique_filename=f"{model_Id}{file_ext}"
    file_path=os.path.join(UPLOAD_DIR,unique_filename)
    try:
        with open(file_path,"wb") as buffer:
            content=await file.read()
            buffer.write(content)
        return{
            "success":True,
            "modelId":model_Id,
            "message":"Model uploaded successfully."
        }
    except Exception as e:
        return{
            "success":False,
            "error":str(e)
        }


            
    