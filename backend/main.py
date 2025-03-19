from fastapi import FastAPI, HTTPException
from config import ai_client, SYS_PROMPT, CONVERSATION_FLOW
from models import CustomPrompt, ChatRequest
import json

app = FastAPI()
system_prompt_with_workflow = SYS_PROMPT + json.dumps(CONVERSATION_FLOW, indent=2)

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
