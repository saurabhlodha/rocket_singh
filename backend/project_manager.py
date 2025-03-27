import os
import subprocess
from typing import Optional

class ProjectManager:
    def __init__(self):
        self.base_port = 8001
        self.running_processes = {}

    def start_project(self, project_name: str) -> Optional[int]:
        """Starts a project's backend server on a unique port"""
        if project_name in self.running_processes:
            return self.base_port + list(self.running_processes.keys()).index(project_name)

        project_dir = f"projects/{project_name}"
        if not os.path.exists(project_dir):
            return None

        port = self.base_port + len(self.running_processes)
        process = subprocess.Popen(
            ["python", "backend/main.py"],
            cwd=project_dir,
            env={**os.environ, "PORT": str(port)}
        )
        
        self.running_processes[project_name] = {
            "process": process,
            "port": port
        }
        
        return port

    def stop_project(self, project_name: str) -> bool:
        """Stops a project's backend server"""
        if project_name not in self.running_processes:
            return False

        process_info = self.running_processes[project_name]
        process_info["process"].terminate()
        process_info["process"].wait()
        del self.running_processes[project_name]
        return True

    def get_project_port(self, project_name: str) -> Optional[int]:
        """Gets the port number for a running project"""
        if project_name in self.running_processes:
            return self.running_processes[project_name]["port"]
        return None

project_manager = ProjectManager()
