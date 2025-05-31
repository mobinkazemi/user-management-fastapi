from fastapi import FastAPI
from db.database import engine, Base

import models_import_order  # DO NOT DELETE THIS LINE

from middleware import rateLimitMiddleware
from middleware.permissionMiddleware import PermissionMiddleware
from router import routes as api_router
from fastapi.middleware.cors import CORSMiddleware
from middleware import checkTokenVerificationMiddleware
from seeder.seeder import seeder

app = FastAPI()
app.add_middleware(rateLimitMiddleware.DBRateLimitMiddleware)
app.add_middleware(PermissionMiddleware)
app.add_middleware(checkTokenVerificationMiddleware.checkTokenVerificationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
app.include_router(api_router)


seeder()
