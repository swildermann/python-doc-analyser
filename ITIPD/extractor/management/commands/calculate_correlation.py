from optparse import make_option

from django.core.management.base import BaseCommand
from extractor.models import *


class Command(BaseCommand):
    help = 'calculates correlation'

    option_list = BaseCommand.option_list + (
        make_option('--percent',
            action='store_true',
            dest='percent',
            default=False,
            help='calculate in percent!'),
        )

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        for knowledge in range(1,13):
            results = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            all_units_with_this_marking = MarkedUnit.objects.filter(user__username="results",knowledge_type=knowledge)\
                .distinct('documentation_unit__id')\
                .values_list('documentation_unit__id',flat=True)
            how_many = len(all_units_with_this_marking)
            results[0]=how_many
            for unit in all_units_with_this_marking:
                other_markings = MarkedUnit.objects.exclude(knowledge_type=knowledge).filter(user__username="results",
                    documentation_unit__id=unit)\
                    .distinct("knowledge_type").values_list("knowledge_type",flat=True)
                for marking in other_markings:
                    results[marking]+=1

            if options['percent']:
                for idx, val in enumerate(results):
                    if how_many>0:
                        results[idx]=val/how_many
                    else:
                        results[idx]=0

            self.stdout.write(str(results))
            self.stdout.write(str(how_many))
            self.stdout.write(str("*****"))

