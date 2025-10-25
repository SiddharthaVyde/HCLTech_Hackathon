from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class EMI(BaseModel):
    principal: Annotated[float, Field(..., gt=0, description="Principal loan amount")]
    loan_type: Annotated[Literal['Education_loan', 'House_loan', 'Car_loan', 'Others'], Field(..., description="Type of loan")]
    tenure_years: Annotated[int, Field(..., gt=0, description="Loan tenure in years")]

    @computed_field
    @property
    def roi(self) -> float:
        if self.loan_type == 'Education_loan':
            return 5.0
        elif self.loan_type == 'House_loan':
            return 6.5
        elif self.loan_type == 'Car_loan':      
            return 9.0
        else:
            return 12.0


    @computed_field
    @property
    def calculate_emi(self) -> float:
        r = self.roi / (12 * 100)
        n = self.tenure_years * 12
        emi = (self.principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return round(emi, 2)
    
@app.post("/apply-loan")
def apply_loan(loan: EMI):
    if loan.principal > 1000000 or loan.tenure_years > 20: #conditions can be changed
        return JSONResponse(content={"status": "denied", "message": "Loan application denied due to eligibility criteria."})
    
    return JSONResponse(
        content={
            "status": "approved",
            "principal": loan.principal,
            "loan_type": loan.loan_type,
            "tenure_years": loan.tenure_years,
            "roi": loan.roi,
            "emi": loan.calculate_emi
        }
    )