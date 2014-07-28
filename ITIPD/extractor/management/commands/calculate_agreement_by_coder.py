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
            
        self.stdout.write("***FINISH***")




