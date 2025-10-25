from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, condecimal
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Enum as SAEnum
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from decimal import Decimal
import enum
import uuid

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class AccountType(str, enum.Enum):
    SAVINGS = "savings"
    CURRENT = "current"
    SALARY = "salary"

MIN_INITIAL_DEPOSIT = {
    AccountType.SAVINGS: 500.00,
    AccountType.CURRENT: 5000.00,
    AccountType.SALARY: 0.00
}

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(36), unique=True, index=True, nullable=False)
    holder_name = Column(String(200), nullable=False)
    account_type = Column(SAEnum(AccountType), nullable=False)
    balance = Column(Numeric(12, 2), nullable=False)

Base.metadata.create_all(bind=engine)

class AccountCreate(BaseModel):
    holder_name: str = Field(..., min_length=1, max_length=200)
    account_type: AccountType
    initial_deposit: float = Field(..., ge=0)

class AccountOut(BaseModel):
    id: int
    account_number: str
    holder_name: str
    account_type: AccountType
    balance: float = Field(..., ge=0)

    class Config:
        orm_mode = True

def generate_account_number() -> str:
    return str(uuid.uuid4()) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Banking API - UUID Account Creation")

@app.post("/accounts", response_model=AccountOut, status_code=201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):

    min_deposit = MIN_INITIAL_DEPOSIT[payload.account_type]
    if float(payload.initial_deposit) < float(min_deposit):
        raise HTTPException(
            status_code=400,
            detail=f"Minimum initial deposit for {payload.account_type.value} is {min_deposit:.2f}"
        )

    acct_no = generate_account_number()

    account = Account(
        account_number=acct_no,
        holder_name=payload.holder_name.strip(),
        account_type=payload.account_type,
        balance=payload.initial_deposit
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    return account

@app.get("/accounts/{account_number}", response_model=AccountOut)
def get_account(account_number: str, db: Session = Depends(get_db)):
    acc = db.query(Account).filter_by(account_number=account_number).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc