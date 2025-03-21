
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from netty.consts import PROJECT_DIR
from fastapi import Request

router = APIRouter()

template_path = f"{PROJECT_DIR}/src/netty/web/templates"
templates = Jinja2Templates(directory=template_path)


@router.get("/")
async def index(request: Request) -> HTMLResponse:
    tools = [
        {
            "name": "FQDN Address Group Generation",
            "description": "Generate FQDN address group configuration",
            "url": "/tools/fqdn-address-group"
        },
        {
            "name": "IP Address Group Generation",
            "description": "Generate IP address group configuration",
            "url": "/tools/ip-address-group"
        }
    ]
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tools": tools}
    )