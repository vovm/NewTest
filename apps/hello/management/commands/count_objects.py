from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = 'Print to console all models and count the objects in every model'

    def handle(self, *args, **options):
        for app in models.get_apps():
            for model in models.get_models(app):
                self.stdout.write('Model %s has %d objects in DB'
                                  % (model.__name__, model.objects.count()))
                self.stderr.write('Error: Model %s has %d objects in DB'
                                  % (model.__name__, model.objects.count()))
