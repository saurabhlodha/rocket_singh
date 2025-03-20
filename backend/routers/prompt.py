from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import SystemPrompt
from validations import SystemPromptUpdate
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/prompts/{name}")
async def get_system_prompt(name: str, db: Session = Depends(get_db)):
    config = db.query(SystemPrompt).filter(SystemPrompt.name == name).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@router.put("/api/prompts/{name}")
async def update_system_prompt(name: str, config_update: SystemPromptUpdate, db: Session = Depends(get_db)):
    prompt = db.query(SystemPrompt).filter(SystemPrompt.name == name).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    prompt.content = config_update.content
    db.commit()
    db.refresh(prompt)
    return prompt
