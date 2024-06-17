from fastapi import FastAPI
from sqladmin import Admin

from app.admin.views import UsersAdmin, CategoriesAdmin, ProductsAdmin, CartsAdmin, CartItemsAdmin
from app.database import engine
from app.users.router import router as router_users
from app.products.router import router as router_products
from app.cart_items.router import router as router_cart_items
from app.cart.router import router as router_cart

app = FastAPI()

app.include_router(router_users)
app.include_router(router_products)
app.include_router(router_cart_items)
app.include_router(router_cart)

admin = Admin(app, engine)

admin.add_view(UsersAdmin)
admin.add_view(ProductsAdmin)
admin.add_view(CategoriesAdmin)
admin.add_view(CartsAdmin)
admin.add_view(CartItemsAdmin)
