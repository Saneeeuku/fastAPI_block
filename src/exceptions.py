class BaseBookingException(Exception):
    detail: str = "Неустановленная ошибка"

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseBookingException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class NoFreeRoomsException(BaseBookingException):
    detail = "Свободных номеров такого типа или в указанный промежуток времени нет"


class DataConflictException(BaseBookingException):
    detail = "Конфликт данных"


class UserConflictException(DataConflictException):
    detail = "Пользователь уже существует"


class LoginException(BaseBookingException):
    detail = "Неверный логин или пароль"


class TokenException(LoginException):
    detail = "Проблема с токеном"


class DateViolationException(BaseBookingException):
    detail = "Некорректные даты"
