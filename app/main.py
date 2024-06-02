from fastapi import FastAPI

from app.users.router import router as router_users
from app.products.router import router as router_products

app = FastAPI()

app.include_router(router_users)
app.include_router(router_products)
