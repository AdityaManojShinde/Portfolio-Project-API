# Portfolio Project API

## Virtual Enviroment Setup
I have used uv to manage virtual enviroment setup in this project.
```python

uv venv # setup virtual enviroment
uv pip install -r requirements.txt # install required modules

```

## Run The API
To run the api use following command.

```python

uvicorn app.main:app  --reload
```

## Projects Route
The API exposes project CRUD operations at the `/project` path.

### Endpoints
### Project
- `GET /project/` - List all projects
- `GET /project/{project_id}` - Get a project by ID
- `POST /project/` - Create a new project
- `PATCH /project/{project_id}` - Update an existing project
- `DELETE /project/{project_id}` - Delete a project
### Authentication
- `POST /auth/login` - Login User And Give Auth Token
### Example Create Request
Send a JSON body with the required fields:

```json
{
  "title": "Deepfake Detection System",
  "description": "A dual-stream CNN model using Vision Transformers.",
  "tech_stack": ["Python", "PyTorch", "FastAPI"],
  "img_url": "https://example.com/project-image.png",
  "github_url": "https://github.com/user/project",
  "live_demo_url": "https://demo.com/project"
}
```

Example curl command:

```bash
curl -X POST "http://127.0.0.1:8000/project/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Deepfake Detection System","description":"A dual-stream CNN model using Vision Transformers.","tech_stack":["Python","PyTorch","FastAPI"],"img_url":"https://example.com/project-image.png","github_url":"https://github.com/user/project","live_demo_url":"https://demo.com/project"}'
```

### API Docs
Once the app is running, open the interactive docs at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`
