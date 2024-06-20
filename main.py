from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "welcome to simlon medical center's backend"}