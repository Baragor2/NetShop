from fastapi import FastAPI

from app.users.router import router as router_users
from app.products.router import router as router_products
from app.cart_items.router import router as router_cart_items
from app.cart.router import router as router_cart

app = FastAPI()

app.include_router(router_users)
app.include_router(router_products)
app.include_router(router_cart_items)
app.include_router(router_cart)