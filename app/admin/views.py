from sqladmin import ModelView

from app.cart.models import Carts
from app.cart_items.models import CartItems
from app.categories.models import Categories
from app.products.models import Products
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [
        Users.name,
        Users.email,
        Users.active,
        Users.role,
        Users.cart,
        Users.cart_item,
    ]
    column_details_exclude_list = [Users.password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class ProductsAdmin(ModelView, model=Products):
    column_list = [column.name for column in Products.__table__.columns] + [
        Products.category,
        Products.cart_item
    ]
    name = "Продукт"
    name_plural = "Продукты"
    icon = "fa-solid fa-store"


class CategoriesAdmin(ModelView, model=Categories):
    column_list = [Categories.id, Categories.name, Categories.product]
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-list"


class CartsAdmin(ModelView, model=Carts):
    column_list = [Carts.id, Carts.username, Carts.user]
    name = "Корзина"
    name_plural = "Корзины"
    icon = "fa-solid fa-cart-shopping"


class CartItemsAdmin(ModelView, model=CartItems):
    column_list = [column.name for column in CartItems.__table__.columns] + [
        CartItems.product,
        CartItems.user
    ]
    name = "Продукт корзины"
    name_plural = "Продукты корзины"
    icon = "fa-solid fa-bars"
