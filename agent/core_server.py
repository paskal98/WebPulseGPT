from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse
from pydantic import BaseModel

from agent.agentGPT import Agent


class Project(BaseModel):
    project_id: str
    name: str
    description: str
    openAIKey: str
    implementation: str
    issue: str


app = FastAPI()


@app.post("/api/project/create")
async def create_project(item: Project):
    agentGPT = Agent(item.openAIKey, item.name, item.description)
    status = agentGPT.agent_start_impl()
    project_id = agentGPT.get_project_id()
    return JSONResponse({'status':status, 'project_id':project_id})

@app.post("/api/project/issue")
async def create_project(item: Project):
    agentGPT = Agent(item.openAIKey, None, None)
    agentGPT.set_project_id(item.project_id)
    status = agentGPT.on_users_update(item.issue)
    return JSONResponse({'status':status, 'project_id':item.project_id})

@app.post("/api/project/update/project_summary")
async def create_project(item: Project):
    agentGPT = Agent(None, None, None)
    agentGPT.set_project_id(item.project_id)
    agentGPT.update_project_summary(item.implementation)
    return JSONResponse({'status':'OK', 'project_id':item.project_id})

@app.get("/api/project/get/buildfile/{project_id}")
async def get_project(project_id: str):
    return FileResponse(path=f"output/projects/{project_id}/build.sh", filename="build.sh")


@app.get("/api/project/get/project_summary/{project_id}")
async def get_project(project_id: str):
    return FileResponse(path=f"output/projects/{project_id}/project_summary.txt", filename="project_summary.txt")
