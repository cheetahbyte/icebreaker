from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# routes
from routes.ct import router as ct_router
app = FastAPI(title="ICEBREAKER")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}

# mount routers
app.include_router(ct_router, prefix="/docker")