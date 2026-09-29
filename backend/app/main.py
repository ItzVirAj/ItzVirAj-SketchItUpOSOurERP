from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .modules.core.router import router as core_router
from .modules.projects.router import router as projects_router
app=FastAPI(title="SketchItUp Owner OS API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(core_router,prefix="/api/v1")
app.include_router(projects_router,prefix="/api/v1/projects",tags=["projects"])
@app.get("/api/v1/health")
def health(): return {"status":"ok","database":"configured"}
