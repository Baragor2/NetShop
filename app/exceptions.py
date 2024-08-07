from fastapi import HTTPException, status


class MarketException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectUsernameOrPasswordException(MarketException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверное имя пользователя или пароль"


class UserIsNotActiveException(MarketException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не активен"


class UserAlreadyExistsException(MarketException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class InvalidTokenException(MarketException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный токен"


class NoSuchProductException(MarketException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такого продукта не существует"


class NoSuchProductInCartException(MarketException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такой продукт в корзине отсутствует"


class NotEnoughRightsException(MarketException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав"


class NoSuchCategoryException(MarketException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такой категории не существует"


class ProductsWithSuchCategoryException(MarketException):
    status_code = status.HTTP_409_CONFLICT
    detail = "С этой категорией существуют продукты"
