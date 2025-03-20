from fastapi import FastAPI, HTTPException
import models
from database import engine
from routers import conversations, chat, prompt

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(conversations.router)
app.include_router(chat.router)
app.include_router(prompt.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
