"""
Import json data from JSON file to Datababse
"""
import os
import json
from recipes.models import Ingredient
from django.core.management.base import BaseCommand
from datetime import datetime
from foodgram.settings import BASE_DIR


class Command(BaseCommand):
    def import_movie_from_file(self):
        data_folder = os.path.join(BASE_DIR, 'recipes', 'resources')
        for data_file in os.listdir(data_folder):
            with open(os.path.join(data_folder, data_file), encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                for data_object in data:
                    name = data_object.get('name', None)
                    measurement_unit = data_object.get('measurement_unit', None)

                    try:
                        ingredient, created = Ingredient.objects.get_or_create(
                            name=name,
                            measurement_unit=measurement_unit
                        )
                        if created:
                            ingredient.save()
                            display_format = "\nMovie, {}, has been saved."
                            print(display_format.format(ingredient))
                    except Exception as ex:
                        print(str(ex))
                        msg = "\n\nSomething went wrong saving this movie: {}\n{}".format(name, str(ex))
                        print(msg)


    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.import_movie_from_file()