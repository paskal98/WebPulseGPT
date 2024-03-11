from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse
from pydantic import BaseModel

from agent.agentGPT import Agent


class Project(BaseModel):
    name: str
    description: str
    dev_plan: str
    implementation: str
    openAIKey: str



app = FastAPI()


@app.post("/api/project/create")
async def create_project(item: Project):
    agentGPT = Agent(item.openAIKey, item.name, item.description)
    status = agentGPT.agent_start_impl()
    project_id  = agentGPT.get_project_id()
    return JSONResponse({'status':status, 'project_id':project_id})


@app.get("/api/project/get/buildfile/{project_id}")
async def get_project(project_id: str):
    return FileResponse(path=f"output/projects/{project_id}/build.sh", filename="build.sh")