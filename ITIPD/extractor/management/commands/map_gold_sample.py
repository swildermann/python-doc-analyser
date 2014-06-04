from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser
import random
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'maps the gold sample'

    def create_mapping(self, object_list, offset, max_elems):

    def handle(self, *args, **options):
        self.stdout.write("***START***")


        Command.create_mapping(self, 30, 3, 89)

