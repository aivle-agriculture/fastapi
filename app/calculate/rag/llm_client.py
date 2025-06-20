import os
import openai
from decimal import Decimal
from app.calculate.schemas import CalculateRequest, CalculateResponse
from app.calculate.rag.rag_workflow import calculate_with_rag
from app.calculate.labels import LABELS

openai.api_key = os.getenv('OPENAI_API_KEY')

async def request_insurance_calculation(request: CalculateRequest) -> CalculateResponse:
    lines = [
        f"보험 품목: {request.insured_item.value}",
        f"작물 종류: {request.crop_type.value}",
        f"보장 종류: {request.coverage_type.value}",
    ]

    # params의 모든 키·값을 한글 라벨과 함께 추가
    for key, val in request.params.items():
        label = LABELS.get(key, key)

        lines.append(f"{label}: {val}")


    lines.append("")
    lines.append("위 정보를 바탕으로 적절하게 보험금 계산을 진행한 뒤, 계산된 보험금을 숫자 형태로만 출력해주세요.")
    lines.append("예시) 123,456")

    prompt = "\n".join(lines)

    result = await calculate_with_rag(request.insured_item, prompt)
    
    # 결과에서 쉼표를 제거하고 Decimal로 변환
    amount_str = result['result'].replace(',', '')
    estimated_amount = Decimal(amount_str)
    
    return CalculateResponse(estimated_amount=estimated_amount)