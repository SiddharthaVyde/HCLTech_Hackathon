from fastapi import FastAPI
from pydantic import BaseModel, computed_field
import pickle
import pandas as pd

with open('model_detect.pkl','rb') as f:
    pipeline = pickle.load(f)

app = FastAPI()

class Transaction(BaseModel):
    Amount: float
    Previous_Balance: float
    Current_Balance: float
    Transaction_Type: str
    Device_Type: str
    Transaction_Frequency_Weekly: str 
    Is_International: int 
    Device_Change: int   

    @computed_field
    @property
    def prev_trans_ratio(self) -> float:
        if self.Previous_Balance == 0:
            return 0.0
        return self.Amount / self.Previous_Balance  

@app.post("/predict")
def predict(tx: Transaction):
    df = pd.DataFrame([tx.model_dump()])
    pred = pipeline.predict(df) 
    anomaly_flag = 1 if pred[0] == -1 else 0
    return {"anomaly": anomaly_flag}