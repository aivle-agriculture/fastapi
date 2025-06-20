from pydantic import BaseModel
from decimal import Decimal
from typing import Dict
from app.calculate.enums import InsuredItem, CropType, CoverageType

# Request 모델
class CalculateRequest(BaseModel):
    insured_item: InsuredItem
    crop_type: CropType
    coverage_type: CoverageType
    params: Dict[str, Decimal]

# Response 모델
class CalculateResponse(BaseModel):
    estimated_amount: Decimal