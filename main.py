from datetime import datetime
import uvicorn
from fastapi import FastAPI, Request, Header
from fastapi.responses import RedirectResponse, JSONResponse
from routers import route

app = FastAPI(description="Learning Middlewares",
              version="0.1")


@app.middleware("http")
async def middleware(request: Request, call_next, x_custom_header=Header(True)):
    response = await call_next(request)
    method = request.method
    url = request.url
    time = datetime.now()

    print("time:", time, "url:", url, "method:", method)

    if not x_custom_header:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing X-Custom-Header"}
        )
    return response


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/hello")
async def hello_route(user: str = "Anonimus"):
    return f"Hello, {user}!"


app.include_router(route, prefix="/movies", tags=["movie"])

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
