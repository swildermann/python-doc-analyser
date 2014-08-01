from optparse import make_option

from django.core.management.base import BaseCommand
from extractor.models import *
from extractor.views import merge_markings, idx_to_dict, get_length_of_marking
from extractor.merge_sample import compare_stretch_with_confusions
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = '''this command calculates for each student the agreement-score to the goldsample'''



    option_list = BaseCommand.option_list + (
        make_option('--confusion',
            action='store_true',
            dest='count',
            default=False,
            help='Get the results including confusion-solution'),
        )

    def compare_stretch(self,first,second, all_indexes):
        #is replaced by compare_stretch_with_confusions
        #will not be deleted as it is may will be needed later
        inside_if=0
        '''check if my is inside of opposite
        check if opposite is inside of my
        check of my and opposite contain each other for at least 50%
        '''
        for my in first:
            for opposite in second:
                state = 0 # 1 = first if is true, 2 = second if is true
                if my[1]>=opposite[1] and my[2]<=opposite[2]:
                    state = 1
                if my[2]>=opposite[1] and my[1]<=opposite[1] and (my[2]-opposite[1])>=((my[2]-my[1])/2):
                    state = 2
                if (state==1 or state==2) and my[3]==opposite[3]:
                    #self.stdout.write(str(my[3]))
                    #self.stdout.write(str(opposite[3]))
                    inside_if+=1
                    all_indexes.update({my[0]:True})
                    all_indexes.update({opposite[0]:True})

        return all_indexes


    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_gold_units = MappingUnitToUser.objects.filter(user__username='goldsample')
        all_users = User.objects.filter(groups__name='Students')

        for user in all_users:
            how_much_true_in_total = 0
            counter=0
            for gold_unit in all_gold_units:
                try:
                    user_unit = MappingUnitToUser.objects.get(user=user,documentation_unit=gold_unit.documentation_unit)
                except MappingUnitToUser.DoesNotExist:
                    continue
                gold_range = MarkedUnit.objects.filter(documentation_unit=gold_unit.documentation_unit,
                                                       user=gold_unit.user).values('id', 'char_range','knowledge_type')
                coders_range = MarkedUnit.objects.filter(documentation_unit=gold_unit.documentation_unit,
                                                         user=user).values('id', 'char_range','knowledge_type')

                counter+=1

                if len(coders_range)==0 and len(gold_range)==0:
                    how_much_true_in_total+=100
                    continue
                if len(coders_range)==0 or len(gold_range)==0:
                    continue

                #self.stdout.write(str(gold_unit.documentation_unit.id))
                my_results = merge_markings(coders_range)
                results_to_compare = merge_markings(gold_range)

                all_idx = {}
                all_idx.update(idx_to_dict(my_results))
                all_idx.update(idx_to_dict(results_to_compare))
                if options['confusion']:
                    compare_stretch_with_confusions(my_results,results_to_compare,all_idx)
                    compare_stretch_with_confusions(results_to_compare,my_results,all_idx)
                else:
                    Command.compare_stretch(self,results_to_compare,my_results,all_idx)
                    Command.compare_stretch(self,my_results,results_to_compare,all_idx)

                trues = 0
                length_of_all_trues = 0
                for key, value in all_idx.items():
                    if value:
                        trues+= 1
                        length_of_all_trues += get_length_of_marking(key, my_results, results_to_compare)


                falses = 0
                length_of_all_false = 0
                for key, value in all_idx.items():
                    if not value:
                        length_of_all_false += get_length_of_marking(key, my_results, results_to_compare)
                        falses+= 1

                total_length = length_of_all_trues + length_of_all_false
                how_much_is_true = round((length_of_all_trues/total_length)*100,5)
                how_much_true_in_total+=how_much_is_true

            self.stdout.write("username:" +str(user.username))
            if counter!=0:
                output=(how_much_true_in_total/counter)
                self.stdout.write(str(output))
                self.stdout.write(str(counter))
            else:
                self.stdout.write("could not compare anything")
            self.stdout.write("***********")

