from extractor.views import *


def calculate_best_goldsample(pk):
    #1- compare 1 and 2
    #2- compare 2 and 3
    #3- compare 3 and 1
    #wenn 1 und 2 am höchsten: id2
    #wenn 1 und 3 am höchsten: id1
    #wenn 2 und 3 am höchsten: id3

    markings1 = merge_markings(MarkedUnit.objects.filter(user__groups__name="validators", documentation_unit__pk=pk,
                                          user__username="prechelt_user")\
                                         .values('id', 'char_range','knowledge_type'))
    markings2 = merge_markings(MarkedUnit.objects.filter(user__groups__name="validators", documentation_unit__pk=pk,
                                          user__username="sven_user")\
                                          .values('id', 'char_range','knowledge_type'))
    markings3 = merge_markings(MarkedUnit.objects.filter(user__groups__name="validators", documentation_unit__pk=pk,
                                          user__username="SchmeiskyZieris")\
                                         .values('id', 'char_range','knowledge_type'))
    if len(markings1)==0 and len(markings2)==0:
        return 100
    if len(markings1)==0 or len(markings2)==0 or len(markings3)==0:
        return 0


    firstAndSecond=get_compatible_in_percent(markings1,markings2)
    secondAndThird=get_compatible_in_percent(markings2,markings3)
    ThirdandFirst=get_compatible_in_percent(markings3,markings1)

    if firstAndSecond>=secondAndThird>=ThirdandFirst:
        return "Sven"
    elif firstAndSecond>=ThirdandFirst>=secondAndThird:
        return "Prechelt"
    elif secondAndThird>=ThirdandFirst>=firstAndSecond:
        return "Schmeisky"
    else:
        return "NIEMAND?"



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
