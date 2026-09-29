from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import get_database_url
app=FastAPI(title="SketchItUp Owner OS API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/api/v1/health")
def health():
    return {"status":"ok","database":"configured" if get_database_url() else "not_configured"}
