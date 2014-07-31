from django.core.management.base import BaseCommand
from extractor.merge_goldsample import *


class Command(BaseCommand):
    help = 'merges the samples of two coders'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.filter(user__groups__name='validators')\
            .distinct('documentation_unit')\
            .values_list('documentation_unit__pk', flat=True)
        status_array = []
        for each in all_units:
            status = calculate_best_goldsample(each)
            status_array.append(status)

        self.stdout.write(str(status_array))