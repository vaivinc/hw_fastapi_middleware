from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request, Body, Header

from starlette.responses import JSONResponse, RedirectResponse


app = FastAPI(description="Learning Middlewares",
              version="0.1")


@app.middleware("http")
async def middleware_root(request: Request, call_next) -> JSONResponse:
    if request.url.path in ["/", "docs", "/openapi.json"]:
        return await call_next(request)

    method = request.method
    url = request.url.path
    time = datetime.now()
    log_message = f"[{time}]: {method} to {url}\n"

    print(log_message)
    with open("log.txt", "a") as f:
        f.write(log_message)

    print(request.headers)

    if "XC-Header" not in request.headers:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing X-Custom-Header"}
        )
    return await call_next(request)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/hello")
async def hello_route(user: str = "Anonimus", xc_header=Header(True)):
    return f"Hello, {user}!"


@app.get("/send/data")
async def hello_route(data: dict = Body({"user": "Name"})):
    return f"{data}!"


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
