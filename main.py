from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "welcome to a go to FastAPI backend"}

@app.get("/wait")
def wait():
    return {"wait": "this works well now"}