from fastapi import FastAPI
import models
from database import engine
from routers import conversations, chat, prompt, project
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(conversations.router)
app.include_router(chat.router)
app.include_router(prompt.router)
app.include_router(project.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
