from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
import datetime, random, ast
from datetime import timedelta
from extractor.models import DocumentationUnit, MarkedUnit, MappingUnitToUser, AccessLog, Agreement
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count



def view_unit(request, pk):
    #it is more a rate than a view now
    documentation_id = pk
    try:
        documentation_unit1 = DocumentationUnit.objects.get(id=documentation_id)
    except DocumentationUnit.DoesNotExist:
        raise Http404
    current_user = request.user
    now = str(datetime.datetime.now())

    access_log = AccessLog.objects.create(
            user=current_user,
            documentation_unit=documentation_unit1,
            timestamp=now,
            filename = "rate_unit")

    marked_units = (MarkedUnit.objects.filter(user=request.user, documentation_unit=documentation_unit1))

    return render(request, 'extractor/detail.html', {'object': documentation_unit1, 'marked_units': marked_units})

def first_next(request):
    unit_list = (MappingUnitToUser.objects.filter(user=request.user, already_marked=False)
                                          .order_by('documentation_unit'))
    current_user = request.user
    if len(unit_list) == 0:
        return render(request, 'extractor/no_units.html')
    unit = unit_list[0]
    now = str(datetime.datetime.now())
    store_unit = DocumentationUnit.objects.get(pk = unit.documentation_unit.id)
    access_log = AccessLog.objects.create(
        user=current_user,
        documentation_unit=store_unit,
        timestamp=now,
        filename="rate_unit")
    return render(request, 'extractor/detail.html', {'object': unit.documentation_unit})

def show_parent(request, pk):
    documentation_id = pk
    try:
        documentation_unit1 = DocumentationUnit.objects.get(id=documentation_id)
    except DocumentationUnit.DoesNotExist:
        raise Http404
    current_user = request.user
    now = str(datetime.datetime.now())

    access_log = AccessLog.objects.create(
            user=current_user,
            documentation_unit=documentation_unit1,
            timestamp=now,
            filename = "parent")
    return render(request, 'extractor/parents.html', {'object': documentation_unit1})


def show_file(request, pk):
    documentation_id = pk
    try:
        documentation_unit1 = DocumentationUnit.objects.get(id=documentation_id)
    except DocumentationUnit.DoesNotExist:
        raise Http404
    current_user = request.user
    now = str(datetime.datetime.now())
    access_log = AccessLog.objects.create(
            user=current_user,
            documentation_unit=documentation_unit1,
            timestamp=now,
            filename = "file")

    filename = str(documentation_unit1.filename)
    parts_of_name = filename.split("/")
    last_part = parts_of_name[-1]
    link = "https://docs.python.org/3/library/" + last_part
    return redirect(link)


@csrf_exempt
@login_required(login_url='/extractor/login/')
def vote(request):
    if request.method != 'POST':
        data = {'error': 'Invalid method'}
        return HttpResponseBadRequest(
            json.dumps(data), content_type='application/json'
        )

    now = str(datetime.datetime.now())
    documentation_id = json.loads(request.POST['unit'])
    documentation_unit1 = DocumentationUnit.objects.get(pk=documentation_id)
    getrange = json.loads(request.POST['range'])
    html = request.POST['html_text']
    current_user = request.user
    ## delete old units if they exist ##
    DeleteOldUnits = MarkedUnit.objects.filter(user=current_user, documentation_unit=documentation_unit1).delete()
    for entry in getrange:
        marked_unit = MarkedUnit.objects.create(
            user=current_user,
            documentation_unit=documentation_unit1,
            knowledge_type=entry['type'],
            html_text=html,
            range=entry['serializedRange'],
            char_range=entry['characterRange'],
            timestamp=now
        )
    mappedunit = MappingUnitToUser.objects.get(documentation_unit=documentation_id, user=current_user)
    mappedunit.already_marked = True
    unmarked_results =  how_much_is_unmarked(request.user, documentation_id)
    mappedunit.unmarked_chars = unmarked_results[0]
    mappedunit.unmarked_percent = unmarked_results[1]
    mappedunit.last_change = now
    mappedunit.save()

    calculate_agreement(request.user,documentation_id)

    return HttpResponse(
        json.dumps({'success': request.POST['range']}),
        content_type='application/json'
    )



@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('extractor/documentationunit_list.html')
        else:
            print("disabled account")
            # TODO Return a 'disabled account' error message
    else:
        print("invalid login")
        # TODO Return an 'invalid login' error message.

@csrf_exempt
@login_required(login_url='')
def show_next_unit(request):
    units = DocumentationUnit.objects.filter(mappingunittouser__user=request.user,
                                             mappingunittouser__already_marked=False)\
                                     .order_by('pk')
    if len(units) == 0:
        return render(request, 'extractor/no_units.html')

    return render(request, 'extractor/next_units.html', {'units': units})

@login_required(login_url='')
def marked_units(request):
    # shows all saved units (also with zero markings)
    units = MappingUnitToUser.objects.filter(user=request.user, already_marked=True)\
                                      .order_by('-documentation_unit__pk')
    return render(request, 'extractor/markedunits.html', {'units': units})

def random_mapping(request):
    #randomly maps a unit with an id between 1 and 8300
    number = random.randint(1, 8300)
    current_user = request.user
    unit = DocumentationUnit.objects.get(pk=number)
    if current_user.is_superuser:
        mapUnitToUser = MappingUnitToUser.objects.create(
            user=current_user,
            documentation_unit=unit,
            already_marked=False,
            last_change =  "1900-01-01 00:00:00",
            unmarked_chars = len(unit.plaintext),
            unmarked_percent = 100
        )
        return render(request, 'extractor/randomunit.html')
    return HttpResponse("You need to be superuser for that..!")

@login_required(login_url='')
def mystats(request):
    a = stats_per_student(request.user)


    return render (request, 'extractor/mystats.html', {'total_marked_units' : a["total_marked_units"],
                                                       'total_unmarked_units' : a["total_unmarked_units"],
                                                       'total_units' : a["total_units"],
                                                       'marked_14' : a["marked_14_count"],
                                                       'marked_8' : a["marked_8_count"],
                                                       'marked_4' : a["marked_4_count"],
                                                       'marked_2' : a["marked_2_count"],
                                                       'agreement_total_count' : a['agreement_total_count'],
                                                       'agreement_total' : a["agreement_total"],
                                                       'agreement_14_count' : a['agreement_14_count'],
                                                       'agreement_14' : a["agreement_14"],
                                                       'agreement_8_count' : a['agreement_8_count'],
                                                       'agreement_8' : a["agreement_8"],
                                                       'agreement_4_count' : a['agreement_4_count'],
                                                       'agreement_4' : a["agreement_4"],
                                                       'agreement_2_count' : a['agreement_2_count'],
                                                       'agreement_2' : a["agreement_2"],
                                                       })

@login_required(login_url='')
def allstats(request):
    total_saved_units = MappingUnitToUser.objects.filter(already_marked=True)\
                                                 .count()
    total_unsaved_units =MappingUnitToUser.objects.filter(already_marked=False)\
                                                 .count()
    total_units = MappingUnitToUser.objects.count()

    marked_units_distinct = MarkedUnit.objects.order_by('documentation_unit__pk')\
                                               .distinct('documentation_unit', 'user')\
                                               .count()
    all_students = User.objects.filter(groups__name='Students')
    all_validators = User.objects.filter(groups__name='validators')

    units_per_validator = {}
    units_per_validator_14 = {}
    units_per_validator_8 = {}
    units_per_validator_4 = {}
    units_per_validator_2 = {}
    for validator in all_validators:
        counter = MappingUnitToUser.objects.filter(already_marked=True, user = validator).count()
        counter_14 = MappingUnitToUser.objects.filter(already_marked=True, user = validator,
                                                   last_change__gte=datetime.datetime.now()-timedelta(days=14)).count()
        counter_8 = MappingUnitToUser.objects.filter(already_marked=True, user = validator,
                                                    last_change__gte=datetime.datetime.now()-timedelta(days=8)).count()
        counter_4 = MappingUnitToUser.objects.filter(already_marked=True, user = validator,
                                                    last_change__gte=datetime.datetime.now()-timedelta(days=4)).count()
        counter_2 = MappingUnitToUser.objects.filter(already_marked=True, user = validator,
                                                    last_change__gte=datetime.datetime.now()-timedelta(days=2)).count()
        units_per_validator.update({validator: [counter, counter_14, counter_8, counter_4, counter_2]})


    units_per_student = {}
    agreement_per_student = {}
    for student in all_students:

        all_stats = stats_per_student(student)
        total_saved = all_stats["total_marked_units"]
        saved_elements_14 = all_stats["marked_14_count"]
        saved_elements_8 = all_stats["marked_8_count"]
        saved_elements_4 = all_stats["marked_4_count"]
        saved_elements_2 = all_stats["marked_2_count"]
        units_per_student.update({student:(total_saved, saved_elements_14, saved_elements_8, saved_elements_4,
        saved_elements_2)})

        total_agreement = all_stats["agreement_total"]
        agreement_14 = all_stats["agreement_14"]
        agreement_8 = all_stats["agreement_8"]
        agreement_4 = all_stats["agreement_4"]
        agreement_2 = all_stats["agreement_2"]
        agreement_per_student.update({student:(total_agreement, agreement_14, agreement_8, agreement_4,
                                               agreement_2)})



    if request.user.is_superuser:
        return render(request, 'extractor/allstats.html', {'total_marked_units' : total_saved_units,
                                                           'total_unmarked_units' : total_unsaved_units,
                                                           'total_units' : total_units,
                                                           'all_distinct' : marked_units_distinct,
                                                           'all_students' : all_students,
                                                           'units_per_student' : units_per_student,
                                                           'agreement_per_student' : agreement_per_student,
                                                           'units_per_validator' : units_per_validator})

    return HttpResponse("You need to be superuser for that..!")


def how_much_is_unmarked(curr_user, pk):
    all_ranges = MarkedUnit.objects.filter(documentation_unit__pk=pk, user = curr_user).values('id', 'char_range')
    unit_attributes = DocumentationUnit.objects.filter(id=pk).values('plaintext')
    data = []
    for each in all_ranges:
        ids = each["id"]
        start= ast.literal_eval(each["char_range"])[0]["characterRange"]["start"]
        end= ast.literal_eval(each["char_range"])[0]["characterRange"]["end"]
        data.append((ids,start,end))
    data.sort(key=lambda tup: tup[1])
    currentPos = 0
    unmarked_chars = 0
    for each in data:
        if each[1]>currentPos:
            unmarked_chars += each[1]-currentPos
        currentPos = each[2]+1
    plaintext = unit_attributes[0]["plaintext"].replace('[something removed here]','')
    length = len(plaintext)
    if currentPos < length:
        unmarked_chars += length-currentPos

    percentage = round((unmarked_chars/length) * 100, 2)
    return unmarked_chars, percentage





def merge_markings(all_ranges):
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
        results.extend(data)
    results = [x for x in results if not x[1] == x[2] ==-1]
    return results


def errors(first,second):
    error = 0
    for id, val in enumerate(first):
        calc = abs(val-second[id])
        if calc == 0:
            pass
        else:
            error += calc

    return error/2  #divide by 2 for double count each error

def calculate_agreement(current_user, pk):
    """
    :param current_user:
    :param pk:
    :return: Boolean - if this action ended with success or not
    """
    try:
        mapped_id = MappingUnitToUser.objects.get(user=current_user, documentation_unit__pk=pk,
                                                 user__groups__name='Students', already_marked=True)
    except (MappingUnitToUser.MultipleObjectsReturned, MappingUnitToUser.DoesNotExist) as e:
        return False

    my_ranges = MarkedUnit.objects.filter(documentation_unit__pk=pk, user = current_user)\
        .values('id', 'char_range','knowledge_type')
    ranges_to_compare = MarkedUnit.objects.filter(documentation_unit__pk=pk).exclude(user=current_user)\
        .values('id', 'char_range', 'knowledge_type')

    how_many = MarkedUnit.objects.exclude(user=current_user )\
        .filter(documentation_unit__pk=pk, user__groups__name='Students')\
        .distinct('user').count()
    if how_many==1:
        id_to_compare = MappingUnitToUser.objects.exclude(user=current_user) \
            .get(documentation_unit__pk=pk, user__groups__name='Students', already_marked=True)
    else:
        #got more than two units
        return False

    try:
        mapped_unit = MappingUnitToUser.objects.get(documentation_unit__pk=pk,user=current_user, already_marked=True)
    except MappingUnitToUser.DoesNotExist:
        #return HttpResponse("This unit is not mapped.")
        return False

    my_results = merge_markings(my_ranges)
    results_to_compare = merge_markings(ranges_to_compare)

    count_markings_me = [0,0,0,0,0,0,0,0,0,0,0,0]
    count_markings_comp = [0,0,0,0,0,0,0,0,0,0,0,0]
    for each in range(0,12):
        get_my = [val for val in my_results if val[3] == each]
        get_co = [val for val in results_to_compare if val[3] == each]
        count_markings_me[each-1] = len(get_my)
        count_markings_comp[each-1]=len(get_co)

    if len(my_results)!=0:
        agree = abs(100-((round(errors(count_markings_me,count_markings_comp)/len(my_results),4))*100))
    elif len(results_to_compare)!=0:
        agree = abs(100-((round(errors(count_markings_me,count_markings_comp)/len(results_to_compare),4))*100))
    else:
        agree = 0

    first_mapping = MappingUnitToUser.objects.get(pk=min(id_to_compare.id, mapped_id.pk))
    second_mapping = MappingUnitToUser.objects.get(pk=max(id_to_compare.id, mapped_id.pk))
    try:
        change_entry = Agreement.objects.get(first=first_mapping, second=second_mapping)
        change_entry.percentage_by_types = agree
        change_entry.save()

    except Agreement.DoesNotExist:
        Agreement.objects.create(
            first = first_mapping,
            second = second_mapping,
            percentage_by_types = agree,
            percentage_by_chars = 0
        )

    return True


def divide(a,b):
    try:
        return a/b
    except:
        return 0


def stats_per_student(current_user):
    total_marked_units = MappingUnitToUser.objects.filter(already_marked=True,
                                                 user=current_user)\
                                                 .count()
    total_unmarked_units = MappingUnitToUser.objects.filter(already_marked=False,
                                                 user=current_user)\
                                                 .count()
    all_units = MappingUnitToUser.objects.filter(user=current_user)
    total_units = all_units.count()
    marked_14 = MappingUnitToUser.objects.filter(already_marked=True, user=current_user,
                                                last_change__gte=datetime.datetime.now()-timedelta(days=14))
    marked_8 = MappingUnitToUser.objects.filter(already_marked=True, user=current_user,
                                                last_change__gte=datetime.datetime.now()-timedelta(days=8))
    marked_4 = MappingUnitToUser.objects.filter(already_marked=True, user=current_user,
                                                last_change__gte=datetime.datetime.now()-timedelta(days=4))
    marked_2 = MappingUnitToUser.objects.filter(already_marked=True, user=current_user,
                                                last_change__gte=datetime.datetime.now()-timedelta(days=2))

    agreement_total = Agreement.objects.filter(Q(first=all_units) | Q(second=all_units))\
        .aggregate(Sum('percentage_by_types'),Count('percentage_by_types'))
    agree_percentage_total  = round(divide(agreement_total["percentage_by_types__sum"],
                         agreement_total["percentage_by_types__count"]),2)
    agreement_14 = Agreement.objects.filter(Q(first=marked_14) | Q(second=marked_14))\
        .aggregate(Sum('percentage_by_types'), Count('percentage_by_types'))
    agree_percentage_14 = round(divide(agreement_14["percentage_by_types__sum"],
                         agreement_14["percentage_by_types__count"]),2)
    agreement_8 = Agreement.objects.filter(Q(first=marked_8) | Q(second=marked_8))\
        .aggregate(Sum('percentage_by_types'), Count('percentage_by_types'))
    agree_percentage_8 = round(divide(agreement_8["percentage_by_types__sum"],
                         agreement_8["percentage_by_types__count"]),2)
    agreement_4 = Agreement.objects.filter(Q(first=marked_4) | Q(second=marked_4))\
        .aggregate(Sum('percentage_by_types'), Count('percentage_by_types'))
    agree_percentage_4 = round(divide(agreement_4["percentage_by_types__sum"],
                         agreement_4["percentage_by_types__count"]),2)
    agreement_2 = Agreement.objects.filter(Q(first=marked_2) | Q(second=marked_2))\
        .aggregate(Sum('percentage_by_types'), Count('percentage_by_types'))
    agree_percentage_2 = round(divide(agreement_2["percentage_by_types__sum"],
                         agreement_2["percentage_by_types__count"]),2)

    marked_14_count= marked_14.count()
    marked_8_count= marked_8.count()
    marked_4_count= marked_4.count()
    marked_2_count= marked_2.count()

    return {'total_marked_units' : total_marked_units,
           'total_unmarked_units' : total_unmarked_units,
           'total_units' : total_units,
           'marked_14_count' : marked_14_count,
           'marked_8_count' : marked_8_count,
           'marked_4_count' : marked_4_count,
           'marked_2_count' : marked_2_count,
           'agreement_total_count' :
               agreement_total["percentage_by_types__count"],
           'agreement_total' : agree_percentage_total,
           'agreement_14_count' :
               agreement_14["percentage_by_types__count"],
           'agreement_14' : agree_percentage_14,
           'agreement_8_count' :
               agreement_8["percentage_by_types__count"],
           'agreement_8' : agree_percentage_8,
           'agreement_4_count' :
               agreement_4["percentage_by_types__count"],
           'agreement_4' : agree_percentage_4,
           'agreement_2_count' :
               agreement_2["percentage_by_types__count"],
           'agreement_2' : agree_percentage_2,
           }