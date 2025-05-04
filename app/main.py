from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date, time

app = FastAPI()

class FormData(BaseModel):
    # Step A
    name: str
    age: int
    phone: str
    email: str
    area: str

    # Step B
    type: str
    date: str  # You can also use `date` if your frontend formats correctly
    time: str  # Likewise, `time` works if properly formatted
    detail: str
    second_name: Optional[str]
    second_age: Optional[int]
    relation: Optional[str]

@app.post("/submit-form")
def submit_form(data: FormData):
    print("✅ Form received:")
    print(data.dict())
    return {"message": "Form submitted successfully", "data": data}
