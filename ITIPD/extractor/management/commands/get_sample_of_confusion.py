from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from extractor.models import *
from django.db.models import Q
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = '<knowledgtype_id, knowledgetype_id>'
    help = 'return 10 units with the users of the given confusion'

    option_list = BaseCommand.option_list + (
        make_option('--count',
            action='store_true',
            dest='count',
            default=False,
            help='Just get the number of units with the given types'),
        )

    def handle(self, *args, **options):
        if len(args)!=2:
            raise CommandError('get_sample_of_confusion takes exactly 2 arguments')
        first_type = KnowledgeType.objects.get(pk=args[0])
        second_type = KnowledgeType.objects.get(pk=args[1])

        if options['count']:
            self.stdout.write(str(Confusions.objects.filter(Q(atype_id=first_type, btype_id=second_type) \
            | Q(atype_id=second_type, btype_id=first_type)).count()))

            return None

        confusion = Confusions.objects.filter(Q(atype_id=first_type, btype_id=second_type) \
            | Q(atype_id=second_type, btype_id=first_type)).order_by("?")[:10]
        for unit in confusion:
            MarkedUnit1 = MarkedUnit.objects.get(pk=unit.idofa.id)
            MarkedUnit2 = MarkedUnit.objects.get(pk=unit.idofb.id)
            DocUnit1 = DocumentationUnit.objects.get(pk=MarkedUnit1.documentation_unit_id)
            DocUnit2 = DocumentationUnit.objects.get(pk=MarkedUnit2.documentation_unit_id)
            if DocUnit1!=DocUnit2:
                raise CommandError('Something went wrong. Trying to compare different documentation units')
            User1 = User.objects.get(pk=MarkedUnit1.user.id)
            User2 = User.objects.get(pk=MarkedUnit2.user.id)
            if User1==User2:
                raise CommandError('can not compare the units of the same user')


            string = User1.username + "|" + User2.username + "|" + str(DocUnit1.id) + "|" + str(DocUnit1.offset) + "|"
            self.stdout.write(string)




        self.stdout.write(str(len(confusion)))
