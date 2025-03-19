from fastapi import FastAPI, HTTPException
import models
from database import engine
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
async def chat(request: ChatRequest):
    try:
        # Create messages array with system prompt
        messages = [{"role": "system", "content": system_prompt_with_workflow}]

        # Add conversation history
        messages.extend([{"role": msg.role, "content": msg.content} 
                        for msg in request.messages])

        # Get response from OpenAI
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return {
            "content": response.choices[0].message.content,
            "role": "assistant"
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
