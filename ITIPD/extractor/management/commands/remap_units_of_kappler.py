from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser
import random, copy
from django.contrib.auth.models import User
"""
map half of the units of Robert Kappler to other students

"""


class Command(BaseCommand):
    help = 'maps 221 units of user robert to the users in group "extra_28"'

    def map_new_and_delete_old(self,doc_unit_id,new_user,old_user):

        doc_unit = DocumentationUnit.objects.get(id=doc_unit_id)

        mapUnitToUser = MappingUnitToUser.objects.create(
            user=new_user,
            documentation_unit=doc_unit,
            already_marked=False,
            last_change =  "1900-01-01 00:00:00",
            unmarked_chars = len(doc_unit.plaintext),
            unmarked_percent = 100
            )

        delete_old = MappingUnitToUser.objects.filter(
            user=old_user,
            documentation_unit=doc_unit
        ).delete()


    def handle(self, *args, **options):

        how_full = {}

        kapplers_units = MappingUnitToUser.objects.filter(user__username="robert", already_marked=False)\
            .order_by("-documentation_unit__id").values_list("documentation_unit__id", flat=True)[:221]

        extra_28 = User.objects.filter(groups__name="extra_28").values_list("username",flat=True)
        extra_28_as_list=[]
        for each in extra_28:
            extra_28_as_list.append(each)
            how_full.update({each:0})

        for each in kapplers_units:
            already_mapped_to = MappingUnitToUser.objects.filter(documentation_unit__id=each)\
                .values_list("user__username", flat=True)
            self.stdout.write("Already mapped to:")
            self.stdout.write(str(already_mapped_to))

            new_students = copy.deepcopy(extra_28_as_list)
            for each in already_mapped_to:
                # do not map a unit to one user twice
                if each in new_students:
                    new_students.remove(each)
                if each == "prechelt_user":
                    new_students.remove('prechelt_extra_28')
                if each == "sven_user":
                    new_students.remove('sven_extra_28')

            random.seed()
            minimum = min(how_full, key=how_full.get)
            if minimum in new_students:
                new_user = minimum
            else:
                new_user=new_students[random.randint(0,len(new_students)-1)]

            how_full[new_user] += 1

            new_user_object = User.objects.get(username=new_user)
            old_user_object = User.objects.get(username="robert")

            self.stdout.write(each)

            #Command.map_new_and_delete_old(self,each,new_user_object,old_user_object)




        self.stdout.write(str(how_full))
