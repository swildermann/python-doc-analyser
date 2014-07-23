from django.core.management.base import BaseCommand, CommandError
from extractor.models import *
from django.db.models import Q
from django.contrib.auth.models import User




class Command(BaseCommand):
    args = '<knowledgtype_id, knowledgetype_id>'
    help = 'return 10 units with the users of the given confusion'

    def handle(self, *args, **options):
        if len(args)!=2:
            raise CommandError('get_sample_of_confusion takes exactly 2 arguments')
        first_type = KnowledgeType.objects.get(pk=args[0])
        second_type = KnowledgeType.objects.get(pk=args[1])
        confusion = Confusions.objects.filter(Q(atype_id=first_type, btype_id=second_type) \
            | Q(atype_id=second_type, btype_id=first_type))
        for unit in confusion:
            DocUnit1 = DocumentationUnit.objects.get(pk=MarkedUnit.objects.get(pk=unit.idofa).documentation_unit_id)
            DocUnit2= DocumentationUnit.objects.get(pk=MarkedUnit.objects.get(pk=unit.idofb).documentation_unit_id)
            if DocUnit1!=DocUnit2:
                raise CommandError('Something went wrong. Trying to compare different documentation units')
            User1 = User.objects.get(pk=MarkedUnit.objects.get(pk=unit.idofa).user_id).username
            User2 = User.objects.get(pk=MarkedUnit.objects.get(pk=unit.idofb).user_id).username
            if User1==User2:
                raise CommandError('can not compare the units of the same user')


            self.stdout.write(User1, User2, DocUnit1)

            self.stdout.write('test')




        self.stdout.write(str(len(confusion)))
