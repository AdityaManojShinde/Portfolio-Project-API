# Portfolio Project API

A comprehensive FastAPI-based backend for a personal portfolio website. It provides endpoints to manage projects, user information, contact details, education, and certifications, all secured via JWT authentication.

## Environment Variables

Before running the API, you need to set up the environment variables. The application requires a `.env` file in the root directory. You can copy the provided `.env.example` file.

```bash
cp .env.example .env
```

Ensure the following variables are set in your `.env` file:
- `SECRET_KEY`: A secure random string for JWT token generation.
- `USERNAME`: The default admin username (created automatically on startup).
- `PASSWORD`: The default admin password (created automatically on startup).

*Note: The application will automatically create a default user with the provided `USERNAME` and `PASSWORD` upon startup if it doesn't already exist.*

## Virtual Environment Setup
I have used `uv` to manage the virtual environment setup in this project.

```bash
uv venv # setup virtual environment
uv pip install -r requirements.txt # install required modules
```

## Run The API
To run the API use the following command:

```bash
uvicorn app.main:app --reload
```

## Authentication

This API uses **OAuth2 with JWT tokens** to protect its routes. Authentication is required for data modification endpoints.

### Login Endpoint
- `POST /auth/login` - Authenticate user and receive JWT token
- `GET /auth/me` - Get current authenticated user info

### Getting a Token

Send a POST request with credentials using OAuth2PasswordRequestForm:

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the `Authorization` header for all protected routes:

```bash
Authorization: Bearer <your_access_token>
```

## API Endpoints

The API exposes multiple CRUD operations to manage different sections of the portfolio. **Data creation, modification, and deletion endpoints require authentication.**

### Projects (`/project`)
- `GET /project/` - List all projects
- `GET /project/{project_id}` - Get a project by ID
- `POST /project/` - Create a new project
- `PATCH /project/{project_id}` - Update an existing project
- `DELETE /project/{project_id}` - Delete a project

### User Info (`/user-info`)
- `GET /user-info/` - Get user information
- `POST /user-info/` - Create user information
- `PATCH /user-info/` - Update user information
- `DELETE /user-info/` - Delete user information

### Contact (`/contact`)
- `GET /contact/` - Get contact details
- `POST /contact/` - Create contact details
- `PATCH /contact/` - Update contact details
- `DELETE /contact/` - Delete contact details

### Education (`/education`)
- `GET /education/` - List all education records
- `GET /education/{education_id}` - Get an education record by ID
- `POST /education/` - Create a new education record
- `PATCH /education/{education_id}` - Update an existing education record
- `DELETE /education/{education_id}` - Delete an education record

### Certification (`/certification`)
- `GET /certification/` - List all certifications
- `GET /certification/{certification_id}` - Get a certification by ID
- `POST /certification/` - Create a new certification
- `PATCH /certification/{certification_id}` - Update an existing certification
- `DELETE /certification/{certification_id}` - Delete a certification

## Example: Create Project with Authentication

1. **Step 1: Login to get token**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

2. **Step 2: Use token to create project**
```bash
curl -X POST "http://127.0.0.1:8000/project/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "title": "Deepfake Detection System",
    "description": "A dual-stream CNN model using Vision Transformers.",
    "tech_stack": ["Python", "PyTorch", "FastAPI"],
    "image_url": "https://example.com/project-image.png",
    "github_link": "https://github.com/user/project",
    "live_demo_link": "https://demo.com/project"
  }'
```

## API Docs
Once the app is running, open the interactive docs at:

- `http://127.0.0.1:8000/docs` - Swagger UI (supports OAuth2 authentication)
- `http://127.0.0.1:8000/redoc` - ReDoc

**In Swagger UI**, you can:
1. Click the "Authorize" button
2. Login with your credentials
3. The token will be automatically included in all requests
