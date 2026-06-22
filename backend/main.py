"""Leapexbiz — 香港持牌 TCSP 公司秘书服务平台
独立后端：服务小程序原型(/tcsp) + 管理后台原型(/admin) + TCSP API(/api/tcsp/*)。
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlmodel import Session, select

from .db import engine, init_db
from . import models as M
from .routers import tcsp as tcsp_router

app = FastAPI(title="Leapexbiz TCSP API", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)
app.include_router(tcsp_router.router)

STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)


@app.on_event("startup")
def on_startup():
    init_db()
    from . import seed
    with Session(engine) as s:
        if not s.exec(select(M.TcspCustomer)).first():
            seed.run(s)


@app.get("/api/health")
def health():
    return {"ok": True, "service": "leapexbiz", "version": "1.0.0"}


@app.get("/")
def root():
    """默认进入小程序原型。"""
    page = STATIC_DIR / "tcsp.html"
    return FileResponse(page) if page.exists() else JSONResponse({"msg": "leapexbiz up"})


@app.get("/tcsp")
def tcsp():
    """Leapexbiz 公司秘书小程序原型。"""
    page = STATIC_DIR / "tcsp.html"
    return FileResponse(page) if page.exists() else JSONResponse({"msg": "tcsp not found"})


@app.get("/admin")
def admin():
    """Leapexbiz 管理后台原型。"""
    page = STATIC_DIR / "admin.html"
    return FileResponse(page) if page.exists() else JSONResponse({"msg": "admin not found"})


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
