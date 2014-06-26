from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser
import random, copy
from django.contrib.auth.models import User
"""
map half of the units of Robert Kappler to other students

"""


class Command(BaseCommand):
    help = 'maps a sample to the 7 students with their id'

    def get_units(self):
        kapplers_units = MappingUnitToUser.objects.filter(user__username="robert", already_marked="False")\
            .order_by("-documentation_unit__id").values_list("documentation_unit__id", flat=True)[:221]

        extra_28 = User.objects.filter(groups__name="extra_28").values_list("username",flat=True)
        for each in kapplers_units:
            already_mapped_to = MappingUnitToUser.objects.filter(documentation_unit__id=each)\
                .values_list("user__username", flat=True)
            self.stdout.write("Already mapped to:")
            self.stdout.write(str(already_mapped_to))

            new_students=[]
            for each in extra_28:
                new_students.append(each)
            for each in already_mapped_to:
                if each in new_students:
                    new_students.remove(each)
                if each == "prechelt_user":
                    new_students.remove('prechelt_extra_28')
                if each == "sven_user":
                    new_students.remove('sven_extra_28')
            self.stdout.write("new students:")
            self.stdout.write(str(new_students))



    def handle(self, *args, **options):

        Command.get_units(self)