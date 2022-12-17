from fastapi import FastAPI

import shopeat.api.accounts.api
from shopeat.api.metadata import OPENAPI_TAGS
import shopeat.api.publish.api
from shopeat.core.database import DATABASE

app = FastAPI(docs_url="/", openapi_tags=OPENAPI_TAGS)

app.include_router(shopeat.api.accounts.api.router)
app.include_router(shopeat.api.publish.api.router)


@app.on_event("startup")
async def init_database():
    await DATABASE.drop_all()
    await DATABASE.create_all()
