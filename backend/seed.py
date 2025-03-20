from models import SystemPrompt
from sqlalchemy.orm import Session
from typing import Any

def create_system_prompt(db: Session, name: str, default_content: Any) -> str:
    config = db.query(SystemPrompt).filter(SystemPrompt.name == name).first()
    if not config:
      config = SystemPrompt(name=name, content=default_content)
      db.add(config)
      db.commit()
      db.refresh(config)

    return config
