from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from decimal import Decimal
from typing import Dict
from enum import Enum
from app.calculate.schemas import CalculateRequest, CalculateResponse
from app.calculate.enums import InsuredItem, CropType, CoverageType
from app.calculate.rag.llm_client import request_insurance_calculation

router = APIRouter()

@router.post("/calc", response_model=CalculateResponse)
async def calculate_insurance(request: CalculateRequest):
    try:
        return await request_insurance_calculation(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))