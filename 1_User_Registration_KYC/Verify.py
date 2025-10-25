from fastapi import UploadFile, File, FastAPI, HTTPException
from User_Registration import users_db

app = FastAPI()

@app.post("/verify_kyc/{user_id}")
def verify_kyc(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not users_db[user_id]["kyc_documents"]:
        raise HTTPException(status_code=400, detail="KYC documents not uploaded yet")
    
    users_db[user_id]["status"] = "VERIFIED"
    return {"message": f"User {user_id} has been verified successfully", "status": "VERIFIED"}