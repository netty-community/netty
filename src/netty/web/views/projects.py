from collections import defaultdict
import os
import logging
from datetime import datetime

from fastapi import APIRouter, Request, Form, HTTPException, Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import yaml

from netty.consts import PROJECT_DIR, TemplateName
from netty.cli.default import (
    generate_default_config_yaml,
    generate_project_yaml,
)
from netty.cli.xlsx_helper import gen_template_xlsx
from netty.gen import gen as generate_config

router = APIRouter()
template_path = f"{PROJECT_DIR}/src/netty/web/templates"
templates = Jinja2Templates(directory=template_path)

logger = logging.getLogger(__name__)


@router.get("")
async def project_list(request: Request):
    """List all projects."""
    projects = defaultdict(list)
    project_dir = PROJECT_DIR / "projects"

    if not project_dir.exists():
        return templates.TemplateResponse(
            "project_list.html", {"request": request, "projects": projects}
        )

    for corp_dir in project_dir.iterdir():
        if not corp_dir.is_dir():
            continue
        for site_dir in corp_dir.iterdir():
            if not site_dir.is_dir():
                continue
            last_modified = site_dir.stat().st_mtime
            projects[corp_dir.name].append(
                {
                    "site_code": site_dir.name,
                    "last_modified": datetime.fromtimestamp(last_modified).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )

    return templates.TemplateResponse(
        "project_list.html", {"request": request, "projects": projects}
    )


@router.get("/new")
async def new_project_form(request: Request):
    return templates.TemplateResponse("project_new.html", {"request": request})


@router.post("/new")
async def create_project(
    request: Request,
    corp_name: str = Form(...),
    site_code: str = Form(...),
    country_code: str = Form(...),
    replace_project_config: bool = Form(True),
):
    try:
        project_dir = PROJECT_DIR / "projects" / corp_name / site_code

        if replace_project_config:
            project_config = {
                "corp_name": corp_name,
                "site_code": site_code,
                "country_code": country_code,
            }
            config_path = PROJECT_DIR / "project.config.yaml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with config_path.open("w", encoding="utf-8-sig") as f:
                yaml.safe_dump(project_config, f, indent=4, sort_keys=False)

        project_dir.mkdir(parents=True, exist_ok=True)

        files_to_create = {
            "project.yaml": generate_project_yaml(),
            "config.yaml": generate_default_config_yaml(country_code),
        }

        for filename, content in files_to_create.items():
            file_path = project_dir / filename
            if not file_path.exists():
                with file_path.open("w", newline="", encoding="utf-8-sig") as f:
                    yaml.safe_dump(content, f, indent=4, sort_keys=False)

        # Create NetworkDesign.xlsx if it doesn't exist
        network_design_path = project_dir / TemplateName.xlsx_file
        if not network_design_path.exists():
            try:
                gen_template_xlsx(country_code, network_design_path)
            except Exception as e:
                logger.error(f"Failed to create NetworkDesign.xlsx: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to create NetworkDesign.xlsx: {str(e)}",
                )

        configuration_dir = project_dir / "configuration"
        configuration_dir.mkdir(parents=True, exist_ok=True)

        configuration_backup_dir = project_dir / "configuration_backup"
        configuration_backup_dir.mkdir(parents=True, exist_ok=True)

        configuration_freeze_dir = project_dir / "configuration_freeze"
        configuration_freeze_dir.mkdir(parents=True, exist_ok=True)

        return RedirectResponse(url="/projects", status_code=303)

    except Exception as _:
        return RedirectResponse(url="/projects/new", status_code=303)


@router.get("/{corp_name}/{site_code}")
async def project_detail(request: Request, corp_name: str, site_code: str):
    """Show project detail page."""
    project_dir = PROJECT_DIR / "projects" / corp_name / site_code
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    # Get files in each directory
    files = {}
    for dir_name in ["configuration", "configuration_backup", "configuration_freeze"]:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            files[dir_name] = sorted(
                [f.name for f in dir_path.iterdir() if f.is_file()]
            )

    return templates.TemplateResponse(
        "project_detail.html",
        {
            "request": request,
            "corp_name": corp_name,
            "site_code": site_code,
            "files": files,
            "current_file": request.query_params.get("file", ""),
        },
    )


@router.get("/{corp_name}/{site_code}/file")
async def get_file_content(corp_name: str, site_code: str, file_path: str):
    """Get file content."""
    project_dir = PROJECT_DIR / "projects" / corp_name / site_code
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    # Only allow viewing .yaml files and files in the specified directories
    allowed_files = {"config.yaml", "NetworkDesign.xlsx", "project.yaml"}
    allowed_dirs = {"configuration", "configuration_backup", "configuration_freeze"}

    # Validate file path
    if not (
        file_path in allowed_files
        or any(file_path.startswith(d + "/") for d in allowed_dirs)
    ):
        raise HTTPException(
            status_code=403, detail="Access to this file is not allowed"
        )

    full_path = project_dir / file_path
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if not full_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    # Check for path traversal
    try:
        full_path.relative_to(project_dir)
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid file path")

    if file_path.endswith(".xlsx"):
        return JSONResponse(
            {"content": "[Excel file content cannot be displayed]", "type": "excel"}
        )

    try:
        with full_path.open("r", encoding="utf-8-sig") as f:
            content = f.read()
            return JSONResponse(
                {
                    "content": content,
                    "type": "yaml" if file_path.endswith(".yaml") else "text",
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{corp_name}/{site_code}/generate")
async def generate_project_config(corp_name: str, site_code: str):
    """Generate configuration for a project."""
    try:
        project_dir = PROJECT_DIR / "projects" / corp_name / site_code
        if not project_dir.exists():
            raise HTTPException(status_code=404, detail="Project not found")

        # TODO: Add your configuration generation logic here
        # For now, just return success
        os.chdir(project_dir)

        # Generate configuration
        generate_config()

        return JSONResponse(
            {"status": "success", "message": "Configuration generated successfully"}
        )

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})

@router.delete("/project")
async def delete_project(
    corp_name: str = Query(..., description="Corporation name"),
    site_code: str | None = Query(None, description="Optional site code. If not provided, deletes entire corporation")
):
    try:
        if site_code:
            # Delete site directory
            project_dir = PROJECT_DIR / "projects" / corp_name / site_code
            if not project_dir.exists():
                raise HTTPException(status_code=404, detail="Project not found")
            
            # Recursively remove the site directory
            import shutil
            shutil.rmtree(project_dir)
            
            # Check if corp directory is empty
            corp_dir = project_dir.parent
            if not any(corp_dir.iterdir()):
                corp_dir.rmdir()
            
            return JSONResponse({"status": "success", "message": f"Project {corp_name}/{site_code} deleted successfully"})
        else:
            # Delete entire corp directory
            corp_dir = PROJECT_DIR / "projects" / corp_name
            if not corp_dir.exists():
                raise HTTPException(status_code=404, detail="Corporation not found")
            
            # Recursively remove the corp directory
            import shutil
            shutil.rmtree(corp_dir)
            
            return JSONResponse({"status": "success", "message": f"Corporation {corp_name} and all its projects deleted successfully"})
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
