from typing import Optional
from fastapi import Depends, FastAPI
from ws.views import wsRouter
from api.views import apiRouter
from core.db import database
from init.views import initRouter
from interface.views import interfaceRoute
import uvicorn
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="1c edo client")

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(interfaceRoute, prefix="", tags=["interface"])
app.include_router(wsRouter, prefix="/ws", tags=["ws"])
app.include_router(apiRouter, prefix="/api", tags=["api"])
app.include_router(initRouter, prefix="/init", tags=["init"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)


