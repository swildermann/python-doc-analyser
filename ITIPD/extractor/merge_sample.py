from extractor.models import *

def compare_stretch_with_confusions(first,second, all_indexes):
    inside_if=0
    '''check if my is inside of opposite
    check if opposite is inside of my
    check of my and opposite contain each other for at least 50%
    '''
    # SELECT AVG(percentage_based_on_chars) from extractor_compatibility;
    for my in first:
        overlap = []
        for opposite in second:
            state = 0 # 1 = first if is true, 2 = second if is true
            if my[1]>=opposite[1] and my[2]<=opposite[2]:
                state = 1
            if my[1]<=my[2]>=opposite[1] and (my[2]-opposite[1])>=((my[2]-my[1])/2):
                state = 2
            if state==1 or state==2:
                if my[3]==opposite[3] \
                        or (my[3]==1 and opposite[3]==4) or (my[3]==4 and opposite[3]==1) \
                        or (my[3]==1 and opposite[3]==2) or (my[3]==2 and opposite[3]==1)\
                        or (my[3]==1 and opposite[3]==12) or (my[3]==12 and opposite[3]==1)\
                        or (my[3]==1 and opposite[3]==10) or (my[3]==10 and opposite[3]==1)\
                        or (my[3]==2 and opposite[3]==7) or (my[3]==7 and opposite[3]==2)\
                        or (my[3]==1 and opposite[3]==8) or (my[3]==8 and opposite[3]==1)\
                        or (my[3]==8 and opposite[3]==9) or (my[3]==9 and opposite[3]==8)\
                        or (my[3]==1 and opposite[3]==6) or (my[3]==6 and opposite[3]==1)\
                        or (my[3]==2 and opposite[3]==4) or (my[3]==4 and opposite[3]==2)\
                        or (my[3]==7 and opposite[3]==8) or (my[3]==8 and opposite[3]==7)\
                        or (my[3]==8 and opposite[3]==4) or (my[3]==4 and opposite[3]==8)\
                        or (my[3]==5 and opposite[3]==7) or (my[3]==7 and opposite[3]==5)\
                        or (my[3]==2 and opposite[3]==5) or (my[3]==5 and opposite[3]==2):
                    inside_if+=1
                    all_indexes.update({my[0]:True})
                    all_indexes.update({opposite[0]:True})
                    break
        #     if state==1:
        #         overlap.append((my[3],opposite[3],my[0],opposite[0],my[2]-my[3]))
        #     if state==2:
        #         overlap.append((my[3],opposite[3],my[0],opposite[0],my[2]-opposite[1]))
        # if len(overlap)>0:
        #     to_save = max(overlap,key=itemgetter(4))
        #     save_confusion(to_save)


    return inside_if


def save_confusion(as_list):
    atype = KnowledgeType.objects.get(id=as_list[0])
    btype = KnowledgeType.objects.get(id=as_list[1])
    aid = MarkedUnit.objects.get(id=(max(as_list[2],as_list[3])))
    bid = MarkedUnit.objects.get(id=(min(as_list[2],as_list[3])))

    try:
        change_entry = Confusions.objects.get(idofa=aid,idofb=bid)
        change_entry.atype = atype
        change_entry.btype = btype
        change_entry.length = as_list[4]
    except Confusions.DoesNotExist:
        Confusions.objects.create(atype=atype,
                                  btype=btype,
                                  idofa=aid,
                                  idofb=bid,
                                  length=as_list[4])
    return True
