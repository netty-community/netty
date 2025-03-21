from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import yaml
from collections import defaultdict
import os
import logging

from netty.consts import PROJECT_DIR, DEFAULT_NETWORK_TEMPLATE_PATH, TemplateName
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

def get_file_tree(directory: Path):
    """Build a tree structure of files and directories."""
    tree = []
    try:
        for item in sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            # Skip hidden files and directories
            if item.name.startswith('.'):
                continue
                
            # Always use full relative path from the root directory
            relative_path = str(item.relative_to(directory)).replace("\\", "/")
            
            node = {
                "name": item.name,
                "path": relative_path,
                "type": "directory" if item.is_dir() else "file"
            }
            
            if item.is_dir():
                children = get_file_tree(item)
                if children:  # Only add directory if it has children
                    node["children"] = children
            
            tree.append(node)
    except Exception as e:
        logger.error(f"Error reading directory {directory}: {e}")
    
    return tree

@router.get("")
async def project_list(request: Request):
    """List all projects."""
    projects = defaultdict(list)
    project_dir = PROJECT_DIR / "projects"

    if project_dir.exists():
        for corp_dir in project_dir.iterdir():
            if corp_dir.is_dir():
                for site_dir in corp_dir.iterdir():
                    if site_dir.is_dir():
                        # Get last modified time
                        last_modified = site_dir.stat().st_mtime
                        # Get template type from config.yaml if it exists
                        config_file = site_dir / "config.yaml"
                        template = ""
                        if config_file.exists():
                            try:
                                with config_file.open() as f:
                                    config = yaml.safe_load(f)
                                    template = config.get("template", "")
                            except Exception:
                                pass

                        projects[corp_dir.name].append({
                                "code": site_dir.name,
                                "template": template,
                            "last_modified": last_modified
                        })
    
    return templates.TemplateResponse(
        "project_list.html",
        {"request": request, "projects": projects}
                        )

@router.get("/new")
async def new_project_form(request: Request):
    return templates.TemplateResponse(
        "project_new.html",
        {"request": request}
    )

@router.post("/new")
async def create_project(
    request: Request,
    corp_name: str = Form(...),
    site_code: str = Form(...),
    country_code: str = Form(...),
    replace_project_config: bool = Form(True)
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

        path = Path(DEFAULT_NETWORK_TEMPLATE_PATH)
        if not path.exists():
            gen_template_xlsx(country_code, project_dir/TemplateName.xlsx_file)
        
        configuration_dir = project_dir / "configuration"
        configuration_dir.mkdir(parents=True, exist_ok=True)

        return JSONResponse({"status": "success", "message": "Project created successfully"})
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

        return JSONResponse({
            "status": "success",
            "message": "Configuration generated successfully"
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        })
