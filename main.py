from typing import Optional
from fastapi import Depends, FastAPI
from endpoints.ws import wsRouter
from endpoints.api import apiRouter
from core.db import database
from endpoints.init import initRouter
from endpoints.interface import interfaceRoute
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="1c edo client")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(interfaceRoute, prefix="", tags=["interface"])
app.include_router(wsRouter, prefix="/ws", tags=["ws"])
app.include_router(apiRouter, prefix="/v1/api", tags=["api"])
app.include_router(initRouter, prefix="/init", tags=["init"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0", reload=True)
    #uvicorn.run(app, port=8000, host="0.0.0.0")#for debug


