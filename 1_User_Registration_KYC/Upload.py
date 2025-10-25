from fastapi import UploadFile, File, FastAPI, HTTPException
from User_Registration import users_db

app = FastAPI()

@app.post("/upload_kyc/{user_id}")
async def upload_kyc(user_id: str, kyc_file: UploadFile = File(...)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[user_id]["kyc_documents"] = kyc_file.filename
    return {"message": f"KYC document '{kyc_file.filename}' uploaded successfully for user {user_id}"}