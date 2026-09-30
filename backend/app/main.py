from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .modules.core.router import router as core_router
from .modules.projects.router import router as projects_router
from .modules.calendar.router import router as calendar_router
from .modules.crm.router import router as crm_router
from .modules.sales.router import router as sales_router
from .modules.finance.router import router as finance_router
from .modules.dashboard.router import router as dashboard_router
from .modules.documents.router import router as documents_router
app=FastAPI(title="SketchItUp Owner OS API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(core_router,prefix="/api/v1")
app.include_router(projects_router,prefix="/api/v1/projects",tags=["projects"])
app.include_router(calendar_router,prefix="/api/v1/calendar",tags=["calendar"])
app.include_router(crm_router,prefix="/api/v1/crm",tags=["crm"])
app.include_router(sales_router,prefix="/api/v1/sales",tags=["sales"])
app.include_router(finance_router,prefix="/api/v1/finance",tags=["finance"])
app.include_router(dashboard_router,prefix="/api/v1/dashboard",tags=["dashboard"])
app.include_router(documents_router,prefix="/api/v1/documents",tags=["documents"])
@app.get("/api/v1/health")
def health(): return {"status":"ok","database":"configured"}
