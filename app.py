from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greet_json():
    return {"Hello": "World!"}

{
  "name": "Python: FastAPI",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/app.py",
  "args": ["run", "--host", "0.0.0.0", "--port", "8000"],
  "console": "integratedTerminal",
  "envFile": "${workspaceFolder}/.env.local.template"
}
