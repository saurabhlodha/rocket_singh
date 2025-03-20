from fastapi import APIRouter, HTTPException
from validations import CustomPrompt
from datetime import datetime

router = APIRouter()

@router.post("/api/prompts")
async def create_prompt(prompt: CustomPrompt):
    try:
        # Here you would typically save to a database
        # For now, we'll just return the prompt
        prompt.timestamp = datetime.now()
        return prompt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
