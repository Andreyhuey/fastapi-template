from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "welcome to simlon medical center's backend"}

@app.get("/wait")
def wait():
    return {"wait": "this works well now"}