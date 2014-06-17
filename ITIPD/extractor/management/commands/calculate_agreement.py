from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser, MarkedUnit
from extractor.views import calculate_agreement



class Command(BaseCommand):
    help = 'calculates the agreement of 2 units'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.all()
        status_array = []
        for each in all_units:
            status = calculate_agreement(each.user,each.documentation_unit.id)
            status_array.append(status)
            self.stdout.write(str(status))

        self.stdout.write(str(status_array))
        self.stdout.write(str(len([x for x in status_array  if x == True])))