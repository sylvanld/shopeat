from fastapi import FastAPI

import shopeat.api.accounts.api
import shopeat.api.publish.api

app = FastAPI(docs_url="/")

app.include_router(shopeat.api.accounts.api.router)
app.include_router(shopeat.api.publish.api.router)
