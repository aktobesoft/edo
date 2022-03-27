from fastapi import FastAPI
from ws.websocket import wsRouter
# from db.base import database
import uvicorn

app = FastAPI(title="1c edo client")
app.include_router(wsRouter, prefix="/ws", tags=["ws"])

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)


