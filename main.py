# main.py - Addition FastAPI Application

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(
    title="Addition API",
    description="A simple API to add two numbers",
    version="1.0.0"
)


class AdditionRequest(BaseModel):
    num1: float
    num2: float


class AdditionResponse(BaseModel):
    num1: float
    num2: float
    result: float
    operation: str


def add_numbers(num1: float, num2: float) -> float:
    """Core logic: return the sum of two numbers."""
    return num1 + num2


@app.get("/", tags=["Health"])
def root():
    return {"message": "Addition API is running. Use /add endpoint."}


@app.get("/add", response_model=AdditionResponse, tags=["Math"])
def add_via_query(
    num1: float = Query(..., description="First number"),
    num2: float = Query(..., description="Second number")
):
    """Add two numbers supplied as query parameters."""
    result = add_numbers(num1, num2)
    return AdditionResponse(num1=num1, num2=num2, result=result, operation="addition")


@app.post("/add", response_model=AdditionResponse, tags=["Math"])
def add_via_body(request: AdditionRequest):
    """Add two numbers supplied in the request body."""
    result = add_numbers(request.num1, request.num2)
    return AdditionResponse(
        num1=request.num1,
        num2=request.num2,
        result=result,
        operation="addition"
    )
