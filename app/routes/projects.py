from fastapi import APIRouter

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

proj_data = [
    {"id": 1, "name": "Project Alpha", "description": "First project"},
    {"id": 2, "name": "Project Beta", "description": "Second project"},
    {"id": 3, "name": "Project Gamma", "description": "Third project"},
    {"id": 4, "name": "Project Delta", "description": "Fourth project"},
]

@router.get("/")
def get_projects():
    """Endpoint to retrieve a list of projects."""
    return {"projects": proj_data}