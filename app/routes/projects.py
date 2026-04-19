from fastapi import APIRouter, HTTPException
from app.models import Project

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

proj_data = [
    {
        "id": 1,
        "title": "Dual-Stream Deepfake Detection",
        "description": "A high-accuracy detection system utilizing Vision Transformers (ViT) and SRM filters to identify spatial and frequency artifacts in manipulated media.",
        "tech_stack": ["Python", "PyTorch", "FastAPI", "Vision Transformers"],
        "img_url": "https://raw.githubusercontent.com/AdityaManojShinde/assets/main/deepfake-detect.png",
        "github_url": "https://github.com/AdityaManojShinde/Deepfake-Detection",
        "live_demo_url": "https://deepfake-check.aditya.dev"
    },
    {
        "id": 2,
        "title": "Shoefy E-Commerce",
        "description": "A full-stack e-commerce platform for sneaker enthusiasts. Features include product management, secure checkout, and a PHP-based admin dashboard.",
        "tech_stack": ["PHP", "MySQL", "JavaScript", "Tailwind CSS"],
        "img_url": "https://raw.githubusercontent.com/AdityaManojShinde/assets/main/shoefy-preview.png",
        "github_url": "https://github.com/AdityaManojShinde/Shoefy",
        "live_demo_url": None
    },
    {
        "id": 3,
        "title": "Student Performance Analytics",
        "description": "A data analytics dashboard built in R to analyze and visualize the correlation between student study habits and academic performance.",
        "tech_stack": ["R", "Shiny", "ggplot2", "Tidyverse"],
        "img_url": "https://raw.githubusercontent.com/AdityaManojShinde/assets/main/r-analytics.png",
        "github_url": "https://github.com/AdityaManojShinde/Student-Performance-R",
        "live_demo_url": None
    }
]

@router.get("/", response_model=list[Project])
def get_all_projects():
    """Endpoint to retrieve a list of projects."""
    # fetch all projects from db 
    projects = proj_data
    return projects

@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int):
    """Endpoint to retrieve a specific project by ID."""
    # Fetch the project with the given ID from db
    project = next((p for p in proj_data if p["id"] == project_id), None)
    # if project is not found, return 404 error
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project