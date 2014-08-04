from django.core.management.base import BaseCommand
from extractor.models import *



class Command(BaseCommand):
    help = 'calculates the agreement of 2 units'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_types = DocumentationUnit.objects.all().distinct("type").values_list("type",flat=True)
        total = [0,0]
        for type in all_types:
            self.stdout.write("*************")
            methods = [0,0]
            fields = [0,0]
            modules = [0,0]
            classes = [0,0]
            describe = [0,0]
            for knowledge in range(1,13):
                self.stdout.write("knowledge-type:"+str(knowledge))
                count_markings = MarkedUnit.objects.filter(user__groups__name="Students",documentation_unit__type=type,
                                          knowledge_type=knowledge).distinct('documentation_unit').count()
                count_units = MappingUnitToUser.objects.filter(user__groups__name="Students",
                                                               documentation_unit__type=type)\
                    .distinct('documentation_unit').count()
                self.stdout.write("markings: "+str(count_markings))
                self.stdout.write("units: "+str(count_units))
                self.stdout.write("in percent: "+str(Command.divide(self,count_markings,count_units)))
                if type=="method" or type=="classmethod" or type=="staticmethod" or type=="function":
                    methods[0]+=count_markings
                    methods[1]+=count_units
                elif type=="attribute" or type=="data":
                    fields[0]+=count_markings
                    fields[1]+=count_units
                elif type=="section":
                    modules[0]+=count_markings
                    modules[1]+=count_units
                elif type=="class" or type=="exception":
                    classes[0]+=count_markings
                    classes[1]+=count_units
                elif type=="describe":
                    describe[0]+=count_markings
                    describe[1]+=count_units
                total[0]+=count_markings
                total[1]+=count_units

            self.stdout.write("methods: "+str(Command.divide(self,methods[0],methods[1])))
            self.stdout.write("fields: "+str(Command.divide(self,fields[0],fields[1])))
            self.stdout.write("modules: "+str(Command.divide(self,modules[0],modules[1])))
            self.stdout.write("classes: "+str(Command.divide(self,classes[0],classes[1])))
            self.stdout.write("describe: "+str(Command.divide(self,describe[0],describe[1])))


        self.stdout.write("in total: "+str(total[0]/total[1]))

    def divide(self,a,b):
        if a==b==0:
            return b
        else:
            return a/b

