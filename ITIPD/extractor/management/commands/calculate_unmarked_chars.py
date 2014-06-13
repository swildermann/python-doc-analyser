from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser, MarkedUnit
from extractor.views import how_much_is_unmarked
import random
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'maps the gold sample'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.all()
        for each in all_units:
            unmarked_results = how_much_is_unmarked(each.user,each.documentation_unit.id)
            self.stdout.write(str(each.documentation_unit.id))
            each.unmarked_chars = unmarked_results[0]
            try:
                each.unmarked_percent = unmarked_results[1]
            except:
                each.unmarked_percent = 999
            each.save()
