import ast

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from extractor.models import MappingUnitToUser, MarkedUnit


class Command(BaseCommand):
    help = 'merges the samples of two coders'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.filter(user__groups__name='Students')\
            .distinct('documentation_unit')
        for unit in all_units:
            first_mapped_id = MappingUnitToUser.objects.get(pk=unit.id)
            all_other_mapped= MappingUnitToUser.objects.exclude(user=first_mapped_id.user)\
                .filter(user__groups__name="Students",
                        documentation_unit=unit.documentation_unit,
                        already_marked=True)
            if len(all_other_mapped)>1:
                raise CommandError("!Found to many mappings to this unit: "+str(unit.documentation_unit.id)+
                                   ". Please have a close look to the code!! "+str(len(all_other_mapped)))
            if len(all_other_mapped)==0:
                self.stdout.write("Found no additional mappings to this unit: "+str(unit.documentation_unit.id)+
                                  " Please have a close look to the code! "+str(len(all_other_mapped)))
                continue
            second_mapped_id = all_other_mapped[0]

            self.stdout.write(".",ending='')
            first_markings = MarkedUnit.objects.filter(user=first_mapped_id.user,
                                                       documentation_unit=first_mapped_id.documentation_unit)\
                                                       .values('id', 'char_range','knowledge_type')
            second_markings = MarkedUnit.objects.filter(user=second_mapped_id.user,
                                                        documentation_unit=second_mapped_id.documentation_unit)\
                                                        .values('id', 'char_range','knowledge_type')
            if len(first_markings)==len(second_markings)==0:
                Command.map_unit(self,unit.documentation_unit)
                continue
            if len(first_markings)==0 or len(second_markings)==0:
                Command.map_unit(self,unit.documentation_unit)
                continue

            first_results = Command.merge_markings_but_hold_idx(self,first_markings)
            second_results = Command.merge_markings_but_hold_idx(self,second_markings)
            Command.is_confusion(self,first_results,second_results,first_mapped_id.user.id,second_mapped_id.user.id)
            #Command.is_confusion(self,second_results,first_results,second_mapped_id.user.id,first_mapped_id.user.id)
            Command.map_unit(self,unit.documentation_unit)





    def is_confusion(self,first,second,first_user_id,second_user_id):
        ranking_list = [15,16,7,4,9,5,8,6,3]
        winner=0 #1 for my and 2 for opposite
        points=[0,0,0]

        #Markierungen vergleichen
        #Bei Konfusion: Pluspunkt vergeben
        #Bei Gleichheit: Gutachter mit mehr Pluspunkten bevorzugen (Markierung übernehmen)
            # (ODER auf "besseren" Gutachter zurückgreifen (Markierung übernehmen))
        #Weder Konfusion noch Gleichheit: Erst Pluspunkte, dann bessere Gutachter

        for my in first:
            for opposite in second:
                if (my[1]>=opposite[1] and my[2]<=opposite[2]) or \
                   (my[2]>=opposite[1] and my[1]<=opposite[1] and (my[2]-opposite[1])>=((my[2]-my[1])/2)) or \
                   (opposite[1]>=my[1] and opposite[2]<=my[2]) or \
                   (opposite[2]>=my[1] and opposite[1]<=my[1] and opposite[2]-my[1]>=((opposite[2]-opposite[1])/2)):
                        is_compatible = Command.confusion_results(self,my[3],opposite[3])
                        if is_compatible >0:
                            points[is_compatible] += 1
                            winner=is_compatible
                        elif is_compatible==0:
                            if points[1]==points[2]:
                                if ranking_list.index(first_user_id)>ranking_list.index(second_user_id):
                                    winner = 1
                                else:
                                    winner = 2
                            else:
                                winner=points.index(max(points[1],points[2]))
                        elif is_compatible==-1:
                            #is not compatible and so nothing will happen as winner is still zero
                            continue
                if winner==1:
                    Command.copy_to_dummy(self,my[0],my[4:])
                elif winner==2:
                    Command.copy_to_dummy(self,opposite[0],opposite[4:])

        return winner



    def copy_to_dummy(self,pk1,pk_rest):

        dummy= User.objects.get(pk=18)
        MarkedObject = MarkedUnit.objects.get(pk=pk1)
        try:
            old_unit = MarkedUnit.objects.exclude(pk=pk1).get(user=dummy,char_range=MarkedObject.char_range,
                                                                           timestamp=MarkedObject.timestamp)
        except MarkedUnit.DoesNotExist:
            MarkedObject.pk = None     #creates a copy of that object
            MarkedObject.user=dummy
            MarkedObject.save()

            for each in pk_rest:
                if each>=:
                    Command.copy_to_dummy(self,each,[])

        return True


    def map_unit(self, unit):
        new_user= User.objects.get(pk=18)
        MappingUnitToUser.objects.create(
            user=new_user,
            documentation_unit = unit,
            already_marked = True,
            last_change =  "1900-01-01 00:00:00",
            unmarked_chars = 888,
            unmarked_percent = 100
        )

    def confusion_results(self,type1,type2):
        who_was_it = -1
        confusion_result =0
        if type1==type2:
            who_was_it = 0
            return who_was_it  #they are the same, no point
        elif (type1==1 and type2==4) or (type1==4 and type2==1):
            #confusion_number = 2
            confusion_result = 1
        elif (type1==1 and type2==2) or (type1==2 and type2==1):
            #confusion_number = 3
            confusion_result = 2
        elif (type1==1 and type2==12) or (type1==12 and type2==1):
            #confusion_number = 5
            confusion_result = 1
        elif (type1==1 and type2==10) or (type1==10 and type2==1):
            #confusion_number = 7
            confusion_result = 1
        elif (type1==2 and type2==7) or (type1==7 and type2==2):
            #confusion_number = 8
            confusion_result = 7
        elif (type1==1 and type2==8) or (type1==8 and type2==1):
            #confusion_number = 10
            confusion_result = 8
        elif (type1==8 and type2==9) or (type1==9 and type2==8):
            #confusion_number = 11
            confusion_result = 9
        elif (type1==1 and type2==6) or (type1==6 and type2==1):
            #confusion_number = 12
            confusion_result = 6
        elif (type1==2 and type2==4) or (type1==4 and type2==2):
            #confusion_number = 13
            confusion_result = 2
        elif (type1==7 and type2==8) or (type1==8 and type2==7):
            #confusion_number = 14
            confusion_result = 8
        elif (type1==8 and type2==4) or (type1==4 and type2==8):
            #confusion_number = 15
            confusion_result = 4
        elif (type1==5 and type2==7) or (type1==7 and type2==5):
            #confusion_number = 16
            confusion_result = 5
        elif (type1==2 and type2==5) or (type1==5 and type2==2):
            #confusion_number = 17
            confusion_result = 2
        else:
            who_was_it = -1
            return who_was_it #no confusion found

       # check who gets the point and which marking is used
        if type1==confusion_result:
            who_was_it=1
        elif type2==confusion_result:
            who_was_it=2
        else:
            self.stdout.write('that should not be possible')

        return who_was_it

    def merge_markings_but_hold_idx(self,all_ranges):
        row_data = []
        results = []
        for each in all_ranges:
            ids = each["id"]
            start= ast.literal_eval(each["char_range"])[0]["characterRange"]["start"]
            end= ast.literal_eval(each["char_range"])[0]["characterRange"]["end"]
            knowledge_type = each["knowledge_type"]
            row_data.append([ids,start,end,knowledge_type])
        row_data.sort(key=lambda tup: tup[1])

        for knowledge_type in range(1,13):
            data = [val for val in row_data if val[3] == knowledge_type]
            for idx, val in enumerate(data):
                if idx+1 >= len(data):
                    break
                if (data[idx+1][1]-data[idx][2]) <= 3 or (data[idx+1][2] <= data[idx][2]):
                       if data[idx][3] == data[idx+1][3]:
                           new_start = min(data[idx][1],data[idx+1][1])
                           new_end = max(data[idx][2],data[idx+1][2])
                           data[idx+1][1] = new_start
                           data[idx+1][2] = new_end
                           data[idx][1] = -1
                           data[idx][2] = -1
                           data[idx+1].append(idx)
            results.extend(data)
        #only keep the merged markings
        results = [x for x in results if not x[1] == x[2] ==-1]
        return results

