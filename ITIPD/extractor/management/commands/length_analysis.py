from optparse import make_option
import math

from django.core.management.base import BaseCommand
from extractor.models import *


class Command(BaseCommand):
    help = 'this is the length analysis'

    option_list = BaseCommand.option_list + (
        make_option('--chars',
            action='store_true',
            dest='chars',
            default=False,
            help='calculate chars!'),
        )

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.filter(user__username="results")\
                                .values_list('documentation_unit__id',flat=True)

        all_length = []
        methods = []
        fields = []
        modules = []
        classes = []
        describe = []
        for unit in all_units:
            doc_unit = DocumentationUnit.objects.get(pk=unit)
            if options['chars']:
                words = len(doc_unit.plaintext)
            else:
                words = len((doc_unit.plaintext).split())

            all_length.append(words)
            type = doc_unit.type

            if type=="method" or type=="classmethod" or type=="staticmethod" or type=="function":
                methods.append(words)
            elif type=="attribute" or type=="data":
                fields.append(words)
            elif type=="section":
                modules.append(words)
            elif type=="class" or type=="exception":
                classes.append(words)
            elif type=="describe":
                describe.append(words)

        self.stdout.write("****average***")
        self.stdout.write("methods: "+str(sum(methods)/len(methods)))
        self.stdout.write("fields: "+str(sum(fields)/len(fields)))
        self.stdout.write("modules: "+str(sum(modules)/len(modules)))
        self.stdout.write("classes: "+str(sum(classes)/len(classes)))
        self.stdout.write("describe: "+str(sum(describe)/len(describe)))
        self.stdout.write("Length of all units together: "+str(sum(all_length)/len(all_length)))

        self.stdout.write("****median***")
        self.stdout.write("methods: "+str(Command.median(self,methods)))
        self.stdout.write("fields: "+str(Command.median(self,fields)))
        self.stdout.write("modules: "+str(Command.median(self,modules)))
        self.stdout.write("classes: "+str(Command.median(self,classes)))
        self.stdout.write("describe: "+str(Command.median(self,describe)))
        self.stdout.write("all units together: "+str(Command.median(self,all_length)))

        self.stdout.write("****lower quartile***")
        self.stdout.write("methods: "+str(Command.lower_quartile(self,methods)))
        self.stdout.write("fields: "+str(Command.lower_quartile(self,fields)))
        self.stdout.write("modules: "+str(Command.lower_quartile(self,modules)))
        self.stdout.write("classes: "+str(Command.lower_quartile(self,classes)))
        self.stdout.write("describe: "+str(Command.lower_quartile(self,describe)))
        self.stdout.write("all units together: "+str(Command.lower_quartile(self,all_length)))

        self.stdout.write("****higher quartile***")
        self.stdout.write("methods: "+str(Command.higher_quartile(self,methods)))
        self.stdout.write("fields: "+str(Command.higher_quartile(self,fields)))
        self.stdout.write("modules: "+str(Command.higher_quartile(self,modules)))
        self.stdout.write("classes: "+str(Command.higher_quartile(self,classes)))
        self.stdout.write("describe: "+str(Command.higher_quartile(self,describe)))
        self.stdout.write("all units together: "+str(Command.higher_quartile(self,all_length)))

        self.stdout.write("****higher quartile***")
        self.stdout.write("methods: "+str(min(methods)))
        self.stdout.write("fields: "+str(min(fields)))
        self.stdout.write("modules: "+str(min(modules)))
        self.stdout.write("classes: "+str(min(classes)))
        self.stdout.write("describe: "+str(min(describe)))
        self.stdout.write("all units together: "+str(min(all_length)))

        self.stdout.write("****higher quartile***")
        self.stdout.write("methods: "+str(max(methods)))
        self.stdout.write("fields: "+str(max(fields)))
        self.stdout.write("modules: "+str(max(modules)))
        self.stdout.write("classes: "+str(max(classes)))
        self.stdout.write("describe: "+str(max(describe)))
        self.stdout.write("all units together: "+str(max(all_length)))

    def median(self,nums):
        nums.sort() #< Sort the list in ascending order
        try:
            mid_num = ( len( nums ) - 1) / 2
            median = nums[ mid_num ]
        except TypeError:   #<  There were an even amount of values
            # Make sure to type results of math.floor/ceil to int for use in list indices
            ceil = int( math.ceil( mid_num ) )
            floor = int( math.floor( mid_num ) )
            median = ( nums[ ceil ] + nums[ floor ] ) / 2
        return median

    def lower_quartile(self,nums):
        nums.sort() #< Sort the list in ascending order
        low_mid = int( round( ( len(nums) + 1 ) / 4.0 ) - 1 ) #< Thanks @Alex (comments)
        lq = nums[low_mid]
        return lq

    def higher_quartile(self,nums):
        nums.sort() #< Sort the list in ascending order
        try:
            high_mid = ( len( nums ) - 1 ) * 0.75
            uq = nums[ high_mid ]
        except TypeError:   #<  There were an even amount of values
            # Make sure to type results of math.floor/ceil to int for use in list indices
            ceil = int( math.ceil( high_mid ) )
            floor = int( math.floor( high_mid ) )
            uq = ( nums[ ceil ] + nums[ floor ] ) / 2
        return uq



