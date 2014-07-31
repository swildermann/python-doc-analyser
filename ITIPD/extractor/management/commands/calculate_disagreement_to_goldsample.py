from django.core.management.base import BaseCommand
from extractor.models import *
from extractor.views import merge_markings
from django.contrib.auth.models import User


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
        for user in User.objects.filter(groups__name='Students').values_list('id',flat=True):
            false_positive = {}
            false_negative = {}
            fits = {}
            for gold_unit in all_gold_units:
                user_unit = MappingUnitToUser.objects.filter(user__id=user,id=gold_unit.id)
                gold_range = MarkedUnit.objects.filter(documentation_unit=gold_unit.documentation_unit,
                                                       user=gold_unit.user).values('id', 'char_range','knowledge_type')
                coders_range = MarkedUnit.objects.filter(documentation_unit=gold_unit.documentation_unit,
                                                         user=user).values('id', 'char_range','knowledge_type')
                if len(coders_range)==0:
                    break

                coders_results = merge_markings(coders_range)
                gold_results = merge_markings(gold_range)

                count_markings_coder = [0,0,0,0,0,0,0,0,0,0,0,0]
                count_markings_gold = [0,0,0,0,0,0,0,0,0,0,0,0]

                for each in range(1,13):
                    #calculate quantity of each knowledge type
                    get_my = [val for val in coders_results if val[3] == each]
                    get_co = [val for val in gold_results if val[3] == each]
                    count_markings_coder[each-1] = len(get_my)
                    count_markings_gold[each-1]=len(get_co)

                bits_of_markings_coder= [Command.greater_zero(self,x) for x in count_markings_coder]
                bits_of_markings_gold = [Command.greater_zero(self,x) for x in count_markings_gold]
                Command.calculate_disagreement(self,bits_of_markings_gold,bits_of_markings_coder,false_positive,false_negative,fits)

            self.stdout.write(str(user))
            self.stdout.write("false positive: "+str(false_positive))
            self.stdout.write("false negative: "+str(false_negative))
            self.stdout.write("correct: "+str(fits))


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
