from django.core.management.base import BaseCommand, CommandError
from extractor.models import *
from extractor.views import calculate_compatiblity



class Command(BaseCommand):
    help = 'calculates the compatibility of 2 units for all students'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.filter(user__groups__name='Students')
        status_array = []
        for each in all_units:
            status = calculate_compatiblity(each.user,each.documentation_unit.id)
            if isinstance(status,basestring):
                status_array.append(status)
            else:
                status_array.append(True)
            #self.stdout.write(str(status))

        self.stdout.write(str(status_array))
        self.stdout.write(str(len([x for x in status_array  if x == True])))