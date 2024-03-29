import re

from django.core.exceptions import ValidationError


def validate_first_last_name(name):
    regex_cyrilic = re.compile(r'^[а-яёА-ЯЁ -]+')
    regex_latin = re.compile(r'^[a-zA-Z -]+')
    if not (regex_cyrilic.fullmatch(name)
            or regex_latin.fullmatch(name)):
        raise ValidationError(
            f'В поле {name} допустимы или только русские, '
            f'или только латинские буквы.'
        )


def validate_username(name):
    """Валидация username."""
    regex_username = re.compile(r'^[\w.@ +-]+')
    if name.lower() == 'me':
        raise ValidationError(
            'Недопустимое имя "me". Придумайте другое имя.'
        )
    if not regex_username.fullmatch(name):
        raise ValidationError(
            f'В поле {name} допустимы только буквы, цифры, '
            f'пробел и знаки @/./+/-/_'
        )


def color_validator(color):
    """Валидация Hex кода цвета."""
    regex_color = re.compile(r'^#([a-fA-F0-9]{6})')
    if not regex_color.fullmatch(color):
        raise ValidationError(
            'Допустим только цветовой HEX-код (например, #49B64E).'
        )
