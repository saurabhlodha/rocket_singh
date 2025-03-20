from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import Conversation
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/conversations")
async def list_conversations(db: Session = Depends(get_db)):
    conversations = db.query(Conversation).order_by(Conversation.started_at.desc()).all()
    return [
        {
            "id": conv.id,
            "started_at": conv.started_at,
            "status": conv.status,
            "last_message": conv.messages[-1].content if conv.messages else None
        }
        for conv in conversations
    ]

@router.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "id": conversation.id,
        "started_at": conversation.started_at,
        "status": conversation.status,
        "messages": [
            {
                "content": msg.content,
                "role": msg.role,
                "timestamp": msg.timestamp
            }
            for msg in conversation.messages
        ],
        "order": {
            "id": conversation.order.id,
            "status": conversation.order.status,
            "specifications": conversation.order.specifications
        } if conversation.order else None
    }
