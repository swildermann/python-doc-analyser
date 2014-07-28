from django.core.management.base import BaseCommand
from extractor.agreements import agreement_by_coder
from django.contrib.auth.models import User



class Command(BaseCommand):
    help = 'calculates the agreement of 2 units'

    def handle(self, *args, **options):
        self.stdout.write("***START***")
        all_students = User.objects.filter(groups__name='Students')
        for student in all_students:
            results = agreement_by_coder(student)
            self.stdout.write(str(results))
            first_part = results[0]
            for key,val in enumerate(first_part):
                if val+results[1][key] != results[2]:
                    self.stdout.write("****CHECKSUM FAILED!")
                    break;
                self.stdout.write("****CHECKSUM PASSED****")

        self.stdout.write("***FINISH***")




