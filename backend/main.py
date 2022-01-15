from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# routes
from routes.ct import router as ct_router
from routes.user import router as user_router, auth_router
# orm
from orm import init
app = FastAPI(title="ICEBREAKER")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}

@app.on_event("startup")
async def startup():
    await init()


# mount routers
app.include_router(ct_router, prefix="/docker")
app.include_router(user_router, prefix="/user")