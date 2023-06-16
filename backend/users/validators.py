import re
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from recipes.models import Tag # Ingredient,


def validate_first_last_name(name):
    regex_cyrilic = re.compile(r'^[а-яёА-ЯЁ -]+')
    regex_latin =re.compile(r'^[a-zA-Z -]+')
    if not (regex_cyrilic.fullmatch(name)
            or regex_latin.fullmatch(name)
    ):
        raise ValidationError(
            f'В поле {name} допустимы или только русские,'
            f'или только латинские буквы.'
        )

def validate_username(name):
    regex_username = re.compile(r'^[\w.@+-]+')
    if name.lower() == 'me':
        raise ValidationError('Недопустимое имя "me". Придумайте другое имя.')
    if not regex_username.fullmatch(name):
        raise ValidationError('Допустимы только буквы, цифры и знаки @/./+/-/_')


def validate_tags(data):
    """Валидация тэгов: отсутствие в request, отсутствие в БД."""
    if not data:
        raise ValidationError({'tags': ['Обязательное поле.']})
    if len(data) < 1:
        raise ValidationError({'tags': ['Хотя бы один тэг должен быть указан.']})
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError({'tags': ['Тэг отсутствует в БД.']})
    return data


def color_validator(color):
    regex_color = re.compile(r'^#([a-fA-F0-9]{6})')
    if not regex_color.fullmatch(color):
        raise ValidationError(
            'Допустим только цветовой HEX-код (например, #49B64E).'
        )

# def validate_ingredients(data):
#     """Валидация ингредиентов и количества."""
#     if not data:
#         raise ValidationError({'ingredients': ['Обязательное поле.']})
#     if len(data) < 1:
#         raise ValidationError({'ingredients': ['Не переданы ингредиенты.']})
#     unique_ingredient = []
#     for ingredient in data:
#         if not ingredient.get('id'):
#             raise ValidationError({'ingredients': ['Отсутствует id ингредиента.']})
#         id = ingredient.get('id')
#         if not Ingredient.objects.filter(id=id).exists():
#             raise ValidationError({'ingredients': ['Ингредиента нет в БД.']})
#         if id in unique_ingredient:
#             raise ValidationError(
#                 {'ingredients': ['Нельзя дублировать имена ингредиентов.']})
#         unique_ingredient.append(id)
#         amount = int(ingredient.get('amount'))
#         if amount < 1:
#             raise ValidationError({'amount': ['Количество не может быть менее 1.']})
#     return data