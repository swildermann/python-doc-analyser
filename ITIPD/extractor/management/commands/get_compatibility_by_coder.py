from django.core.management.base import BaseCommand
from extractor.models import *
from django.db.models import Q
from django.contrib.auth.models import *


class Command(BaseCommand):
    help = 'get compatibility by coders'

    def handle(self, *args, **options):


        print("userid  : username :  chars    : compatible")
        for each in User.objects.filter(groups__name='Students'):
            percentage_chars = Command.get_avg(self,Compatibility.objects.filter(Q(one__user__groups__name='Students'),
                                                  (Q(one__user__id=each.id)|Q(two__user__id=each.id)))\
                .values_list('percentage_based_on_chars',flat=True))

            percentage_compatible = Command.get_avg(self,Compatibility.objects.filter(Q(one__user__groups__name='Students'),
                                                  (Q(one__user__id=each.id)|Q(two__user__id=each.id)))\
                .values_list('percentage_compatible',flat=True))


            print(str(each.id)+": "+each.username+": "+str(percentage_chars)+": "+str(percentage_compatible))


    def get_avg(self,list):
        sum =0
        for each in list:
            sum+=each
        if len(list)==sum==0:
            return 0

        return sum/len(list)