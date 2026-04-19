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

uuvicorn app.main:app  --reload
```