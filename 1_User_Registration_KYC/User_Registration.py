from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import Dict

app = FastAPI()

users_db: Dict[str, dict] = {}

class PersonalDetails(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")

@app.post("/register")
def register_user(details: PersonalDetails):
    if details.user_id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users_db[details.user_id] = {
        "name": details.name,
        "email": details.email,
        "phone": details.phone,
        "status": "UNVERIFIED",
        "kyc_documents": None
    }
    return {"message": "User registered successfully", "status": "UNVERIFIED"}