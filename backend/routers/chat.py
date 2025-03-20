from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import Conversation
from sqlalchemy.orm import Session
from models import Conversation, Message, SystemPrompt
from config import ai_client
from validations import ChatRequest
from config import SYS_PROMPT, CONVERSATION_FLOW, OPENAI_MODEL
from seed import create_system_prompt
import json

router = APIRouter()

def system_prompt_with_workflow(db: Session) -> str:
    system_prompt = create_system_prompt(db=db, name='system_prompt', default_content=SYS_PROMPT).content
    conversation_flow = create_system_prompt(db=db, name='conversation_flow', default_content=CONVERSATION_FLOW).content

    return system_prompt + json.dumps(conversation_flow, indent=2)

@router.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation()
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Create messages array with system prompt
        messages = [{"role": "system", "content": system_prompt_with_workflow(db)}]
        messages.extend([{"role": msg.role, "content": msg.content} for msg in request.messages])

        # Get response from OpenAI
        response = ai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        # Save the new messages to the database
        new_message = Message(
            conversation_id=conversation.id,
            content=request.messages[-1].content,
            role="user"
        )
        db.add(new_message)

        assistant_message = Message(
            conversation_id=conversation.id,
            content=response.choices[0].message.content,
            role="assistant"
        )
        db.add(assistant_message)
        db.commit()

        return {
            "content": response.choices[0].message.content,
            "role": "assistant",
            "conversation_id": conversation.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
