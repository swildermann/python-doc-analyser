from django.core.management.base import BaseCommand
from extractor.models import *
from django.db.models import Q


class Command(BaseCommand):
    help = 'get agreement-values sorted by categorie/type of the units'

    def handle(self, *args, **options):
        self.stdout.write("***START***")
        all_categories = ["exception","attribute","class","method","data","function","staticmethod","section",
                          "classmethod","describe"]
        results = {}
        for categorie in all_categories:
            get_values = Agreement.objects.filter(Q(first_id__documentation_unit__type=categorie) |
                                                  Q(second_id__documentation_unit__type=categorie),
                                                  Q(first_id__user__groups__name="Students")).\
                values_list('percentage_by_types',flat=True)
            results.update({categorie:Command.get_avg(self,get_values)})

        self.stdout.write(str(results))
        self.stdout.write("***FINISH***")


    def get_avg(self,list):
        sum =0
        for each in list:
            sum+=each
        if len(list)==sum==0:
            return 0

        return sum/len(list)