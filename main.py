import asyncio
import time
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request, Body
from fastapi.responses import RedirectResponse
from routers import route

app = FastAPI(description="Learning Middlewares",
              version="0.1")


@app.middleware("http")
async def middleware_root(request: Request, call_next):

    if request.url.path.startswith("/users"):
        response = await call_next(request)
        response.headers["Some"] = "Ist users"
        return response

    print(f"[{datetime.now()}] -- ({request.method}) path: {request.url.hostname}{request.url.path}")

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/hello")
async def hello_rout(user: str = "Anonimus"):
    await asyncio.sleep(0.2)
    return f"Hello, {user}!"


app.include_router(route, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
