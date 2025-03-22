from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from netty.arch.device_role import get_all_device_role_views
from netty.arch.platform import get_platform_views

router = APIRouter()
templates = Jinja2Templates(directory="src/netty/web/templates")

@router.get("/")
async def get_arch_page(request: Request):
    device_roles = get_all_device_role_views()
    platforms = get_platform_views()
    return templates.TemplateResponse(
        "arch/index.html",
        {
            "request": request,
            "device_roles": device_roles,
            "platforms": platforms
        }
    )
