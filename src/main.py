from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main_route():
    return {"message": "moi"}


@app.get("/other")
def ohter():
    return {"message": "other"}
