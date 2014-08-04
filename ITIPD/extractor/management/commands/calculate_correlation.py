from django.core.management.base import BaseCommand
from extractor.models import *



class Command(BaseCommand):
    help = 'calculates correlation'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        for knowledge in range(1,13):
            results = [0,0,0,0,0,0,0,0,0,0,0,0]
            all_units_with_this_marking = MarkedUnit.objects.filter(user__username="results",knowledge_type=knowledge)\
                .distinct('documentation_unit__id')\
                .values_list('documentation_unit__id',flat=True)
            for unit in all_units_with_this_marking:
                other_markings = MarkedUnit.objects.exclude(knowledge_type=knowledge).filter(user__username="results",
                    documentation_unit__id=unit)\
                    .distinct("knowledge_type").values_list("knowledge_type",flat=True)
                for marking in other_markings:
                    results[marking-1]+=1
            self.stdout.write(str(results))

