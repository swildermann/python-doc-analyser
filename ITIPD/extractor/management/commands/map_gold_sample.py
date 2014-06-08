from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser
import random
from django.contrib.auth.models import User
from django.db.models import Q


class Command(BaseCommand):
    help = 'maps the gold sample'
    
    def create_mapping(self,object_list,debug,number):
        random.shuffle(object_list)
        object_list = object_list[:number]
        self.stdout.write("counting:"+str(len(object_list)))
        self.stdout.write(str(object_list))
        all_validaters = User.objects.filter(groups__name='validaters')
        for object in object_list:
            unit=DocumentationUnit.objects.get(id=object)
            for validater in all_validaters:
                if debug==False:
                    mapUnitToUser = MappingUnitToUser.objects.create(
                        user=validater,
                        documentation_unit=unit,
                        already_marked=False,
                        last_change =  "1900-01-01 00:00:00",
                        unmarked_chars = len(unit.plaintext),
                        unmarked_percent = 100
                    )

    def handle(self, *args, **options):
        self.stdout.write("***START***\n")
        ClassOrException = list(MappingUnitToUser.objects.filter(Q(user__groups__name="Students"),
                             Q(documentation_unit__type="class") | Q(documentation_unit__type="exception")) \
                            .distinct("documentation_unit") \
                            .values_list("documentation_unit__pk", flat=True))

        AttributeOrData = list(MappingUnitToUser.objects.filter(Q(user__groups__name="Students"),
                            Q(documentation_unit__type="attribute") | Q(documentation_unit__type="data")) \
                            .distinct("documentation_unit") \
                            .values_list("documentation_unit__pk", flat=True))

        MethodOrFunction = list(MappingUnitToUser.objects.filter(Q(user__groups__name="Students"),
                            Q(documentation_unit__type="method") | Q(documentation_unit__type="staticmethod") | \
                            Q(documentation_unit__type="classmethod") | Q(documentation_unit__type="function")) \
                            .distinct("documentation_unit") \
                            .values_list("documentation_unit__pk", flat=True))

        Describe = list(MappingUnitToUser.objects.filter(Q(user__groups__name="Students"),
                    Q(documentation_unit__type="describe")) \
                    .distinct("documentation_unit") \
                    .values_list("documentation_unit__pk", flat=True))

        Section = list(MappingUnitToUser.objects.filter(Q(user__groups__name="Students"),
                    Q(documentation_unit__type="section")) \
                    .distinct("documentation_unit") \
                    .values_list("documentation_unit__pk", flat=True))

        Command.create_mapping(self, ClassOrException,False,17)
        Command.create_mapping(self, AttributeOrData, False, 30)
        Command.create_mapping(self, MethodOrFunction, False, 88)
        Command.create_mapping(self, Describe, False, 1)
        Command.create_mapping(self, Section, False, 32)

        self.stdout.write("***END***")


