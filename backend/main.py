from fastapi import FastAPI, HTTPException, Depends
import models
from database import engine, get_db
from models import Conversation, Message, Order
from sqlalchemy.orm import Session
from config import ai_client, SYS_PROMPT, CONVERSATION_FLOW
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

system_prompt_with_workflow = SYS_PROMPT + json.dumps(CONVERSATION_FLOW, indent=2)

class MessageBase(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    conversation_id: Optional[int]
    messages: List[MessageBase]


class ConversationResponse(BaseModel):
    id: int
    started_at: datetime
    status: str
    messages: List[Dict]

class CustomPrompt(BaseModel):
    content: str
    timestamp: Optional[datetime] = None


@app.post("/api/chat")
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
        messages = [{"role": "system", "content": system_prompt_with_workflow}]
        messages.extend([{"role": msg.role, "content": msg.content} for msg in request.messages])

        # Get response from OpenAI
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
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

@app.post("/api/prompts")
async def create_prompt(prompt: CustomPrompt):
    try:
        # Here you would typically save to a database
        # For now, we'll just return the prompt
        prompt.timestamp = datetime.now()
        return prompt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
