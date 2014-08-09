from django.core.management.base import BaseCommand
from extractor.models import *
from extractor.views import merge_markings
from django.contrib.auth.models import User
from collections import defaultdict


class Command(BaseCommand):
    help = '''this command calculates for each student how many times (and in percent) he *disagreed* to the goldsample
           'will be calculated for each knowledge-type'''


    def greater_zero(self,y):
        if y>0:
            return 1
        else:
            return 0


    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_gold_units = MappingUnitToUser.objects.filter(user__username='goldsample')
        in_total_pos = {}
        in_total_neg = {}
        all_users = User.objects.filter(groups__name='Students')
        big_counter =0
        false_positive = {}
        false_negative = {}
        fits = {}
        counter=0
        for gold_unit in all_gold_units:
            # try:
            #     user_unit = MappingUnitToUser.objects.get(user=user,documentation_unit=gold_unit.documentation_unit)
            # except MappingUnitToUser.DoesNotExist:
            #     continue


            gold_range = MarkedUnit.objects.filter(documentation_unit=gold_unit.documentation_unit,
                                                   user=gold_unit.user).values('id', 'char_range','knowledge_type')
            coders = MarkedUnit.objects.filter(documentation_unit=gold_unit.documentation_unit,
                                                     user__groups__name="Students")\
                                                     .values_list('user',flat=True)
            if len(coders)!=2:
                self.stdout.write(" This unit is mapped to only so many students: "+str(len(coders)))

            bits = Command.merge_coders_range(self,coders,gold_unit.documentation_unit)


            counter+=1
            gold_results = merge_markings(gold_range)
            #count_markings_coder = [0,0,0,0,0,0,0,0,0,0,0,0]
            count_markings_gold = [0,0,0,0,0,0,0,0,0,0,0,0]

            for each in range(1,13):
                #calculate quantity of each knowledge type
                get_co = [val for val in gold_results if val[3] == each]
                count_markings_gold[each-1]=len(get_co)

            bits_of_markings_coder= Command.merge_coders_range(self,coders,gold_unit.documentation_unit)
            bits_of_markings_gold = [Command.greater_zero(self,x) for x in count_markings_gold]
            Command.calculate_disagreement(self,bits_of_markings_gold,bits_of_markings_coder,false_positive,false_negative,fits)
        in_total_pos=Command.d_sum(self,in_total_pos,false_positive)
        in_total_neg=Command.d_sum(self,in_total_neg,false_negative)
        big_counter+=counter
        #self.stdout.write(str(user.username)+" ** "+str(user.id))
        self.stdout.write("false positive: "+str(false_positive))
        self.stdout.write("false negative: "+str(false_negative))
        self.stdout.write("correct: "+str(fits))
        self.stdout.write("counter: "+str(counter))


        self.stdout.write("total pos:: "+str(in_total_pos))
        self.stdout.write("total neg:: "+str(in_total_neg))
        self.stdout.write("total counter: "+str(big_counter))


    def calculate_disagreement(self,first,second,false_pos,false_neg,correct):
        #first input is goldsample (the better one)

        for idx,val in enumerate(first):
            if val==second[idx]:
                correct.update({idx+1:correct.get(idx+1,0)+1})
            if val==0 and second[idx]==1:
                false_pos.update({idx+1:false_pos.get(idx+1,0)+1})
            elif val==1 and second[idx]==0:
                #false negative
                false_neg.update({idx+1:false_neg.get(idx+1,0)+1})
        return None

    def d_sum(self,a, b):
        d = defaultdict(int, a)
        for k, v in b.items():
            d[k] += v
        return dict(d)

    def merge_coders_range(self,users,unit):

        coders_range_a = MarkedUnit.objects.filter(documentation_unit=unit,user=users[0])\
            .values('id', 'char_range','knowledge_type')
        coders_range_b = MarkedUnit.objects.filter(documentation_unit=unit,user=users[1])\
            .values('id', 'char_range','knowledge_type')
        results_a = merge_markings(coders_range_a)
        results_b = merge_markings(coders_range_b)

        count_markings_a = [0,0,0,0,0,0,0,0,0,0,0,0]
        count_markings_b = [0,0,0,0,0,0,0,0,0,0,0,0]

        for each in range(1,13):
            #calculate quantity of each knowledge type
            get_a = [val for val in results_a if val[3] == each]
            get_b = [val for val in results_b if val[3] == each]
            count_markings_a[each-1] = len(get_a)
            count_markings_b[each-1]=len(get_b)

        bits_of_a = [Command.greater_zero(self,x) for x in count_markings_a]
        bits_of_b = [Command.greater_zero(self,x) for x in count_markings_b]
        result_bits = [0,0,0,0,0,0,0,0,0,0,0,0]

        for idx,val in enumerate(bits_of_a):
            if val==bits_of_b[idx]:
                result_bits[idx]=val
            else:
                result_bits[idx]=99 #dummy value for unequal

        return result_bits
