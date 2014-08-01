from django.core.management.base import BaseCommand
from extractor.models import *
from extractor.views import merge_markings, idx_to_dict, get_length_of_marking
from extractor.merge_sample import compare_stretch_with_confusions
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = '''this command calculates for each student the agreement-score to the goldsample'''


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
                    self.stdout.write("thats it!?")
                    continue


                my_results = merge_markings(coders_range)
                results_to_compare = merge_markings(coders_range)

                all_idx = {}
                all_idx.update(idx_to_dict(my_results))
                all_idx.update(idx_to_dict(results_to_compare))

                comp2 = compare_stretch_with_confusions(results_to_compare,my_results,all_idx)
                compatible = compare_stretch_with_confusions(my_results,results_to_compare,all_idx)
                compatible += comp2


                trues = 0
                length_of_all_trues = 0
                for key, value in all_idx.items():
                    if value:
                        trues+= 1
                        length_of_all_trues += get_length_of_marking(key, my_results, results_to_compare)

                falses = 0
                length_of_all_false = 0
                for key, value in all_idx.items():
                    if value==False:
                        length_of_all_false += get_length_of_marking(key, my_results, results_to_compare)
                        falses+= 1


                total_length = length_of_all_trues + length_of_all_false
                how_much_is_true = round((length_of_all_trues/total_length)*100,5)
                self.stdout.write(str(user.username)+":"+str(how_much_is_true))
                how_much_true_in_total+=how_much_is_true

            self.stdout.write("username:" +str(user.username))
            if counter!=0:
                output=(how_much_true_in_total/counter)
                self.stdout.write(str(output))
                self.stdout.write(str(counter))
            else:
                self.stdout.write("null")
            self.stdout.write("***********")
