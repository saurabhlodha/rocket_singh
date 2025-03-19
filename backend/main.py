from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

# Load conversation flow from a file (you'll need to create this)
with open("backend/conversation_flow.json", "r") as f:
    CONVERSATION_FLOW = json.load(f)

class Message(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    messages: List[Message]

class CustomPrompt(BaseModel):
    content: str
    timestamp: Optional[datetime] = None

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Convert the messages to OpenAI format
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Add system message with sales agent instructions
        system_message = {
            "role": "system",
            "content": """You are a Sales Assistant for Sorpetaler Fensterbau specializing in wooden and wood-aluminium
            window quotes. Guide users in a structured way while keeping conversation natural.
            Follow the conversation flow structure while adapting to user responses.
            Ask one question at a time and confirm details before proceeding."""
        }
        
        messages.insert(0, system_message)
        
        # Call OpenAI API
        response = client.chat.completions.create(
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