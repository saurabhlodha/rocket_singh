from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import Conversation
from sqlalchemy.orm import Session
from project_manager import ProjectManager

router = APIRouter()

@router.post("/api/projects/{project_name}/start")
async def start_project(project_name: str):
    port = project_manager.start_project(project_name)
    if port:
        return {"status": "success", "port": port}
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/api/projects/{project_name}/stop")
async def stop_project(project_name: str):
    if project_manager.stop_project(project_name):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/projects/{project_name}/port")
async def get_project_port(project_name: str):
    port = project_manager.get_project_port(project_name)
    if port:
        return {"port": port}
    raise HTTPException(status_code=404, detail="Project not running")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
