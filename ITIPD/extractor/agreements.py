from extractor.models import *


def agreement_by_coder(current_user):
    all_mapped_units = MappingUnitToUser.objects.filter(user=current_user).values_list('documentation_unit__id',flat=True)
    results = [0,0,0,0,0,0,0,0,0,0,0,0]
    control_results = [0,0,0,0,0,0,0,0,0,0,0,0]
    count = len(all_mapped_units)
    for unit in all_mapped_units:
        for type in range(1,13):
            get_my_marking = MarkedUnit.objects.filter(user=current_user,documentation_unit__id=unit,knowledge_type=type,
                                                       user__groups__name='Students')\
                .values_list('id',flat=True)
            get_opposite_marking = MarkedUnit.objects.exclude(user=current_user).filter(documentation_unit__id=unit,
                                                                                        knowledge_type=type,
                                                                                        user__groups__name='Students')\
                .values_list('id',flat=True)
            if (len(get_my_marking)>0 and len(get_opposite_marking)>0) or (len(get_my_marking)==len(get_opposite_marking)==0):
                results[type-1]+=1
            else:
                control_results[type-1]+=1

    return  results, control_results, count
