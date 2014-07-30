from django.core.management.base import BaseCommand
from extractor.models import *
from django.db.models import Q


class Command(BaseCommand):
    help = 'get compatibility-values sorted by categorie/type of the units'

    def handle(self, *args, **options):
        if args[0]=="0":
            self.stdout.write("return by chars")
            Command.by_chars(self)
        if args[0]=="1":
            self.stdout.write("return by markings")
            Command.by_markings(self)

    def get_avg(self,list):
        sum =0
        for each in list:
            sum+=each
        if len(list)==sum==0:
            return 0

        return sum/len(list)


    def by_chars(self):
        self.stdout.write("***START***")
        all_categories = ["exception","attribute","class","method","data","function","staticmethod","section",
                          "classmethod","describe"]
        results = {}
        for categorie in all_categories:
            get_values = Compatibility.objects.filter(Q(one_id__documentation_unit__type=categorie) |
                                                  Q(two_id__documentation_unit__type=categorie),
                                                  Q(one_id__user__groups__name="Students"),
                                                  Q(two_id__user__groups__name='Students')).\
                values_list('percentage_compatible',flat=True)
            results.update({categorie:Command.get_avg(self,get_values)})

        self.stdout.write(str(results))
        self.stdout.write('methods: '+str((results["method"]+results["classmethod"]+results["staticmethod"]+results["function"])/4))
        self.stdout.write('fields: '+str((results["attribute"]+results["data"])/2))
        self.stdout.write('modules: '+str((results["section"])/1))
        self.stdout.write('classes: '+str((results["class"]+results["exception"])/2))
        self.stdout.write('describe: '+str((results["describe"])/1))
        self.stdout.write("***FINISH***")

    def by_markings(self):
        self.stdout.write("***START***")
        all_categories = ["exception","attribute","class","method","data","function","staticmethod","section",
                          "classmethod","describe"]
        results = {}
        for categorie in all_categories:
            get_values = Compatibility.objects.filter(Q(one_id__documentation_unit__type=categorie) |
                                                  Q(two_id__documentation_unit__type=categorie),
                                                  Q(one_id__user__groups__name="Students"),
                                                  Q(two_id__user__groups__name='Students')).\
                values_list('percentage_based_on_chars',flat=True)
            results.update({categorie:Command.get_avg(self,get_values)})

        self.stdout.write(str(results))
        self.stdout.write('methods: '+str((results["method"]+results["classmethod"]+results["staticmethod"]+results["function"])/4))
        self.stdout.write('fields: '+str((results["attribute"]+results["data"])/2))
        self.stdout.write('modules: '+str((results["section"])/1))
        self.stdout.write('classes: '+str((results["class"]+results["exception"])/2))
        self.stdout.write('describe: '+str((results["describe"])/1))
        self.stdout.write("***FINISH***")