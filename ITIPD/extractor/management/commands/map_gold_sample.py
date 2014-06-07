from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser
import random
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'maps the gold sample'
    def create_mapping(self,object_list):
        self.stdout.write("***START***")
        all_validaters = User.objects.filter(groups__name='validaters')
        for object in object_list:
            for validater in all_validaters:
                mapUnitToUser = MappingUnitToUser.objects.create(
                    user=validater,
                    documentation_unit=object.documentation_unit,
                    already_marked=False,
                    last_change =  "1900-01-01 00:00:00",
                    unmarked_chars = len(object.documentation_unit.plaintext),
                    unmarked_percent = 100
                )
        self.stdout.write("***END***")

    def handle(self, *args, **options):
        # TODO: Only get distinct documentation_units
        #TODO: It maps to many units (+78 more than it should - why!?!) 
        ClassOrException = (MappingUnitToUser.objects.filter(documentation_unit__type='class',
                                                             user__groups__name="Students")) | \
                           MappingUnitToUser.objects.filter(documentation_unit__type='exception',
                                                            user__groups__name="Students") \
                            .order_by('?')[:17]
        AttributeOrData = (MappingUnitToUser.objects.filter(documentation_unit__type='attribute',
                                                             user__groups__name="Students") | \
                           MappingUnitToUser.objects.filter(documentation_unit__type='error',
                                                            user__groups__name="Students")) \
                            .order_by('?')[:30]
        MethodOrFunction = (MappingUnitToUser.objects.filter(documentation_unit__type='method',
                                                             user__groups__name="Students") | \
                           MappingUnitToUser.objects.filter(documentation_unit__type='staticmethod',
                                                            user__groups__name="Students") |\
                           MappingUnitToUser.objects.filter(documentation_unit__type='classmethod',
                                                            user__groups__name="Students") |\
                           MappingUnitToUser.objects.filter(documentation_unit__type='function',
                                                            user__groups__name="Students"))  \
                           .order_by('?')[:88]
        Describe = (MappingUnitToUser.objects.filter(documentation_unit__type='describe',
                                                     user__groups__name="Students")) \
                            .order_by('?')[:1]
        Section = (MappingUnitToUser.objects.filter(documentation_unit__type='section',
                                                    user__groups__name="Students")) \
                            .order_by('?')[:32]
        Command.create_mapping(self, ClassOrException)
        Command.create_mapping(self, AttributeOrData)
        Command.create_mapping(self, MethodOrFunction)
        Command.create_mapping(self, Describe)
        Command.create_mapping(self, Section)




