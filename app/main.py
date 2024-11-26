from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI(title="Catalog Management API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from .routers import (
    suppliers,
    catalogs,
    imports,
    mappings,
    exports
)

app.include_router(suppliers.router, prefix="/api/suppliers", tags=["suppliers"])
app.include_router(catalogs.router, prefix="/api/catalogs", tags=["catalogs"])
app.include_router(imports.router, prefix="/api/imports", tags=["imports"])
app.include_router(mappings.router, prefix="/api/mappings", tags=["mappings"])
app.include_router(exports.router, prefix="/api/exports", tags=["exports"])

@app.get("/")
async def root():
    return {"message": "Welcome to Catalog Management API"}
