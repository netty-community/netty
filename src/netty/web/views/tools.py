from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from netty.consts import PROJECT_DIR

router = APIRouter()
template_path = f"{PROJECT_DIR}/src/netty/web/templates"
templates = Jinja2Templates(directory=template_path)

@router.get("/tools")
async def tools_index(request: Request):
    return templates.TemplateResponse(
        "tools.html",
        {"request": request}
    )

@router.get("/tools/address-group")
async def address_group_page(request: Request, type: str = "fqdn"):
    if type not in ["fqdn", "ip"]:
        type = "fqdn"
    return templates.TemplateResponse(
        "address_group.html",
        {"request": request, "type": type}
    )

@router.post("/tools/address-group")
async def address_group_generate(
    request: Request,
    type: str = Form(...),
    group_name: str = Form(...),
    fqdns: str = Form(None),
    subnets: str = Form(None),
    cache_ttl: int = Form(3600)
):
    if type == "fqdn":
        items = [f.strip() for f in (fqdns or "").split('\n') if f.strip()]
        result = {
            "fqdns": items,
            "group_name": group_name,
            "cache_ttl": cache_ttl
        }
    else:
        items = [s.strip() for s in (subnets or "").split('\n') if s.strip()]
        result = {
            "subnets": items,
            "group_name": group_name
        }
    
    return templates.TemplateResponse(
        "address_group.html",
        {"request": request, "type": type, "result": result}
    )