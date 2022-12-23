from fastapi import FastAPI

import shopeat.api.accounts.api
import shopeat.api.groups.api
import shopeat.api.ingredients.api
import shopeat.api.publish.api
import shopeat.api.recipes.api
from shopeat.api.metadata import (
    OPENAPI_DESCRIPTION,
    OPENAPI_TAGS,
    OPENAPI_TITLE,
    OPENAPI_VERSION,
)
from shopeat.core.database import DATABASE

app = FastAPI(
    title=OPENAPI_TITLE,
    description=OPENAPI_DESCRIPTION,
    version=OPENAPI_VERSION,
    docs_url="/",
    openapi_tags=OPENAPI_TAGS,
)

app.include_router(shopeat.api.accounts.api.router)
app.include_router(shopeat.api.groups.api.router)
app.include_router(shopeat.api.ingredients.api.router)
app.include_router(shopeat.api.recipes.api.router)
app.include_router(shopeat.api.publish.api.router)


@app.on_event("startup")
async def init_database():
    await DATABASE.drop_all()
    await DATABASE.create_all()
