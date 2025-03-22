from fastapi import APIRouter

from netty.web.views.index import router as index_router
from netty.web.views.projects import router as projects_router
from netty.web.views.tools import router as tools_router
from netty.web.views.arch import router as arch_router


def register_views() -> APIRouter:
    root_router = APIRouter()
    root_router.include_router(index_router, tags=["index"])
    root_router.include_router(projects_router, prefix="/projects", tags=["projects"])
    root_router.include_router(tools_router, tags=["tools"])
    root_router.include_router(arch_router, prefix="/arch", tags=["architecture"])
    return root_router


views = APIRouter()
views.include_router(register_views(), prefix="")
