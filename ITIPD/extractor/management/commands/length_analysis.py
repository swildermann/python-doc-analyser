from optparse import make_option

from django.core.management.base import BaseCommand
from extractor.models import *


class Command(BaseCommand):
    help = 'this is the length analysis'

    option_list = BaseCommand.option_list + (
        make_option('--chars',
            action='store_true',
            dest='chars',
            default=False,
            help='calculate chars!'),
        )

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.filter(user__username="results")\
                                .values_list('documentation_unit__id',flat=True)

        all_length = []
        methods = []
        fields = []
        modules = []
        classes = []
        describe = []
        for unit in all_units:
            doc_unit = DocumentationUnit.objects.get(pk=unit)
            words = len((doc_unit.plaintext).split())
            all_length.append(words)
            type = doc_unit.type

            if type=="method" or type=="classmethod" or type=="staticmethod" or type=="function":
                methods.append(words)
            elif type=="attribute" or type=="data":
                fields.append(words)
            elif type=="section":
                modules.append(words)
            elif type=="class" or type=="exception":
                classes.append(words)
            elif type=="describe":
                describe.append(words)


        self.stdout.write("methods: "+str(sum(methods)/len(methods)))
        self.stdout.write("fields: "+str(sum(fields)/len(methods)))
        self.stdout.write("modules: "+str(sum(modules)/len(methods)))
        self.stdout.write("classes: "+str(sum(classes)/len(methods)))
        self.stdout.write("describe: "+str(sum(describe)/len(methods)))
        self.stdout.write("Length of all units together: "+str(sum(all_length)/len(all_length)))
        self.stdout.write("Length of all units together: "+str(sum(all_length)))

        self.stdout.write("*****DEBUG INFORMATION")
        self.stdout.write(str(all_length))
