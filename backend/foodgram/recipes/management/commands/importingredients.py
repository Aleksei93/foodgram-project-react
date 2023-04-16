import csv
import json
import mimetypes
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Импортирует ингридиенты"
    filename: str
    mimetype: str

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", type=str, help="Путь к файлу с данными")
        parser.add_argument(
            "--keep-existing-data", action="store_true",
            help="Предварительная очистка данных модели Ingredients")

    def __load_data_from_file(self, filename, mimetype):
        with open(filename, newline='') as fp:
            try:
                if mimetype == "text/csv":
                    data = csv.DictReader(
                        fp, fieldnames=("name", "measurement_unit"))
                else:
                    data = json.load(fp)
            except (json.decoder.JSONDecodeError, TypeError):
                self.stderr.write(f"Файл {filename} содержит ошибки")
                raise SystemExit

            for item in data:
                yield item

    def handle(self, *args, **options):
        filename = options.get("filename")
        wipe_data = not options.get("keep-exisiting-data")

        if not os.path.isfile(filename):
            self.stderr.write(f"Файл {filename} не найден")
            raise SystemExit

        mimetype = mimetypes.MimeTypes().guess_type(filename)[0]

        if mimetype not in ("text/csv", "application/json"):
            self.stderr.write(f"Файл {filename} имеет запрещенный формат")
            raise SystemExit

        if wipe_data:
            Ingredient.objects.all().delete()

        for item in self.__load_data_from_file(filename, mimetype):
            obj = Ingredient(**item)
            obj.save()
