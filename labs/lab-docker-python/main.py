from fastapi import FastAPI
import platform
import os

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Python Dockerized FastAPI Application",
        "python_version": platform.python_version(),
        "hostname": os.uname().nodename,
        
        }

@app.get("/health")
def health():
    return {"status": "ok"}
