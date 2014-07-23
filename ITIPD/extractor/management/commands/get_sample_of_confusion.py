from django.core.management.base import BaseCommand, CommandError
from extractor.models import *
from django.db.models import Q




class Command(BaseCommand):
    args = '<knowledgtype_id, knowledgetype_id>'
    help = 'return 10 units with the users of the given confusion'

    def handle(self, *args, **options):
        if len(args)!=2:
            raise CommandError('get_sample_of_confusion takes exactly 2 arguments')
        first_type = KnowledgeType.objects.get(pk=args[0])
        second_type = KnowledgeType.objects.get(pk=args[1])
        new = Confusions.objects.filter(Q(atype_id=first_type, btype_id=second_type) \
            | Q(atype_id=second_type, btype_id=first_type)).count()

        self.stdout.write(str(new))

        #, btype_id=args[1]) | (btype_id=args[0], atype_id=args[1]))




        self.stdout.write('Jop')

        # self.stdout.write("***START***")
        #
        # all_units = MappingUnitToUser.objects.all()
        # status_array = []
        # for each in all_units:
        #     status = calculate_agreement(each.user,each.documentation_unit.id)
        #     status_array.append(status)
        #     self.stdout.write(str(status))
        #
        # self.stdout.write(str(status_array))
        # self.stdout.write(str(len([x for x in status_array  if x == True])))