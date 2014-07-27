from extractor.views import *


def calculate_best_goldsample(pk):
    #1- compare 1 and 2
    #2- compare 2 and 3
    #3- compare 3 and 1
    #wenn 1 und 2 am höchsten: id2
    #wenn 1 und 3 am höchsten: id1
    #wenn 2 und 3 am höchsten: id3

    original_1 = MarkedUnit.objects.filter(user__groups__name="validators", documentation_unit__pk=pk,
                                          user__username="prechelt_user")\
                                         .values('id', 'char_range','knowledge_type','user')
    markings1=merge_markings(original_1)
    original_2 = MarkedUnit.objects.filter(user__groups__name="validators", documentation_unit__pk=pk,
                                          user__username="sven_user")\
                                          .values('id', 'char_range','knowledge_type','user')
    markings2=merge_markings(original_2)
    original_3 = MarkedUnit.objects.filter(user__groups__name="validators", documentation_unit__pk=pk,
                                          user__username="SchmeiskyZieris")\
                                         .values('id', 'char_range','knowledge_type','user')
    markings3=merge_markings(original_3)
    if len(markings1)==0 and len(markings2)==0 and len(markings3):
        return "wayne"
    if len(markings1)==0 or len(markings2)==0 or len(markings3)==0:
        return "difficult!"


    firstAndSecond=get_compatible_in_percent(markings1,markings2)
    secondAndThird=get_compatible_in_percent(markings2,markings3)
    ThirdAndFirst=get_compatible_in_percent(markings3,markings1)

    if firstAndSecond>=ThirdAndFirst and secondAndThird>=ThirdAndFirst:
        copy_to_dummy(original_2)
        return "Sven "+str(max(firstAndSecond,secondAndThird))
    elif firstAndSecond>=secondAndThird and ThirdAndFirst>=secondAndThird:
        copy_to_dummy(original_1)
        return "Prechelt "+str(max(firstAndSecond,ThirdAndFirst))
    elif secondAndThird>=firstAndSecond and ThirdAndFirst>=firstAndSecond:
        copy_to_dummy(original_3)
        return "Schmeisky "+str(max(secondAndThird,ThirdAndFirst))
    else:
        return "NIEMAND?"


    #copy all markings of the best user to the dummy "goldsample" with ID 17
    #also map this unit to "goldsample"
    #if markings do already exist: delete them first
    #if mapping already exist: set already_marked to false!



def get_compatible_in_percent(ranges1,ranges2):

    all_idy = {}
    all_idy.update(idx_to_dict(ranges1))
    all_idy.update(idx_to_dict(ranges2))

    compatible = compare_stretch(ranges1,ranges2,all_idy) + compare_stretch(ranges2,ranges1,all_idy)
    #compatilbe counts the number of compatible markings

    trues = 0
    length_of_all_true = 0
    for key, value in all_idy.items():
        if value:
            trues+= 1
            length_of_all_true += get_length_of_marking(key, ranges1, ranges2)

    falses = 0
    length_of_all_falses = 0
    for key, value in all_idy.items():
        if value==False:
            length_of_all_falses += get_length_of_marking(key, ranges1, ranges2)
            falses+= 1


    total_length = length_of_all_true + length_of_all_falses
    percentage_based_on_chars = round((length_of_all_true/total_length)*100,5)


    return percentage_based_on_chars

def copy_to_dummy(markings):
    dummy= User.objects.get(pk=17)

    for every in markings:
        every.pk = None     #creates a copy of that object
        every.user=dummy
        every.save()
        doc_unit = every.documentation_unit

    map_unit(dummy,doc_unit)

    return True


def map_unit(new_user,unit_id):

    MappingUnitToUser.objects.create(
        user=new_user,
        documentation_unit = unit_id,
        already_marked = False,
        last_change =  "1900-01-01 00:00:00",
        unmarked_chars = 999,
        unmarked_percent = 100
    )