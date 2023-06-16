import csv
import os
import sys

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Загрузка данных в БД'
    TABLES = (
        ('ingredients.csv', Ingredient,
            ('name', 'measurement_unit')),
        ('tags.csv', Tag,
            ('name', 'color', 'slug'))
    )

    def handle(self, *args, **options):
        print('--Начинаем импорт данных--')
        # path = os.path.join(settings.BASE_DIR, 'ingredients.csv')
        # при таком путь получается ./backend/ingredients.csv
        # а файлы по ТЗ в ./data/

        for csv_name, model, fields in self.TABLES:
            try:
                csv_file = open(
                    os.path.join('data', csv_name),
                    'r',
                    encoding='utf-8'
                )
            except FileNotFoundError:
                print(f'Файл {csv_name} не найден.')
                sys.exit()
            except OSError:
                print('Произошла ошибка операционной системы '
                      f'при попытке открыть файл {csv_name}.')
                sys.exit()
            except Exception as err:
                print(f'Неожиданная ошибка при открытии файла {csv_name}: ',
                      repr(err))
                sys.exit()
            else:
                with csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)
                    data_map = {}
                    obj = []
                    for row in reader:
                        for i in range(len(fields)):
                            data_map[fields[i]] = row[i]
                        obj.append(model(**data_map))
                    model.objects.bulk_create(obj)
                    print(f'Импорт из файла {csv_name} выполнен.')
        print('--Все импорты прошли успешно--')