from django.core.management.base import BaseCommand, CommandError
from extractor.models import DocumentationUnit, MappingUnitToUser
import random
from django.contrib.auth.models import User
"""
map each unit to 2 different users
"""


class Command(BaseCommand):
    help = 'maps a sample to the 7 students with their id'

    def create_mapping(self, object_list, offset):
        howfull= [0 for x in range(7)]
        user1 = 0
        user2 = 0
        for each in object_list:
            random.seed()

            user1=random.randint(0,6)
            howfull[user1] += 1

            user2=howfull.index(min(howfull))
            howfull[user2] += 1

            user_object1 = User.objects.get(id=(user1)+offset)
            user_object2 = User.objects.get(id=(user2)+offset)
            mapUnitToUser = MappingUnitToUser.objects.create(
                user=user_object1,
                documentation_unit=each,
                already_marked=False
            )
            mapUnitToUser = MappingUnitToUser.objects.create(
                user=user_object2,
                documentation_unit=each,
                already_marked=False
            )
            self.stdout.write(str(howfull))
        self.stdout.write(str(howfull))
        self.stdout.write("***DONE***")

    def handle(self, *args, **options):
        self.stdout.write("***START***")
        ClassOrException = (DocumentationUnit.objects.filter(type='class') | \
                           DocumentationUnit.objects.filter(type='exception')).order_by('?')[:265]
        AttributeOrData = (DocumentationUnit.objects.filter(type='attribute') | \
                          DocumentationUnit.objects.filter(type='data')).order_by('?')[:306]
        MethodOrFunction = (DocumentationUnit.objects.filter(type='method') | \
                           DocumentationUnit.objects.filter(type='staticmethod') | \
                           DocumentationUnit.objects.filter(type='classmethod') | \
                           DocumentationUnit.objects.filter(type='function')).order_by('?')[:651]
        Describe = (DocumentationUnit.objects.filter(type='describe')).order_by('?')[:16]
        Section = (DocumentationUnit.objects.filter(type='section')).order_by('?')[:310]

        self.stdout.write('Counted ClassOrException: "%s"' % ClassOrException.count())
        self.stdout.write('Counted AttributeOrData: "%s"' % AttributeOrData.count())
        self.stdout.write('Counted MethodOrFunction: "%s"' % MethodOrFunction.count())
        self.stdout.write('Counted Describe: "%s"' % Describe.count())
        self.stdout.write('Counted Section: "%s"' % Section.count())
        self.stdout.write('Random-Test: "%s"' % ClassOrException[0].id)

        Command.create_mapping(self, ClassOrException, 3, 76)
        Command.create_mapping(self, AttributeOrData, 3, 88)
        Command.create_mapping(self, MethodOrFunction, 3, 186)
        Command.create_mapping(self, Describe, 3, 5)
        Command.create_mapping(self, Section, 3, 89)

