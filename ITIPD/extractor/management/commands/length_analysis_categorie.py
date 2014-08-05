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
        methods = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
        fields = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
        modules = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
        classes = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
        describe = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

        for unit in all_units:
            doc_unit = DocumentationUnit.objects.get(pk=unit)
            type = doc_unit.type
            how_many_different_markings = MarkedUnit.objects.filter(user__username="results",documentation_unit__id=unit).distinct("knowledge_type").count()
            words = len((doc_unit.plaintext).split())

            if type=="method" or type=="classmethod" or type=="staticmethod" or type=="function":
                methods[how_many_different_markings].append(words)
            elif type=="attribute" or type=="data":
                fields[how_many_different_markings].append(words)
            elif type=="section":
                modules[how_many_different_markings].append(words)
            elif type=="class" or type=="exception":
                classes[how_many_different_markings].append(words)
            elif type=="describe":
                describe[how_many_different_markings].append(words)

        for each in methods:
            self.stdout.write(str(Command.calculate_all(self,each)))


    def median(self,nums):
        #found at https://blog.dlasley.net/2013/01/medians-and-quartiles-in-python/
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
        #found at https://blog.dlasley.net/2013/01/medians-and-quartiles-in-python/
        nums.sort() #< Sort the list in ascending order
        low_mid = int( round( ( len(nums) + 1 ) / 4.0 ) - 1 ) #< Thanks @Alex (comments)
        lq = nums[low_mid]
        return lq

    def higher_quartile(self,nums):
        #found at https://blog.dlasley.net/2013/01/medians-and-quartiles-in-python/
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


    def calculate_all(self,nums):
        return Command.median(self,nums),Command.lower_quartile(self,nums),Command.higher_quartile(self,nums),min(nums),max(nums)