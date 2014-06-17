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
from django.db.models import Q



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
    total_marked_units = MappingUnitToUser.objects.filter(already_marked=True,
                                                 user=request.user)\
                                                 .count()
    total_unmarked_units = MappingUnitToUser.objects.filter(already_marked=False,
                                                 user=request.user)\
                                                 .count()
    total_units = MappingUnitToUser.objects.filter(user=request.user)\
                                                 .count()
    marked_8 = MappingUnitToUser.objects.filter(already_marked=True, user=request.user,
                                                last_change__gte=datetime.datetime.now()-timedelta(days=8)).count()
    marked_4 = MappingUnitToUser.objects.filter(already_marked=True, user=request.user,
                                                last_change__gte=datetime.datetime.now()-timedelta(days=4)).count()
    marked_2 = MappingUnitToUser.objects.filter(already_marked=True, user=request.user,
                                                last_change__gte=datetime.datetime.now()-timedelta(days=2)).count()

    return render (request, 'extractor/mystats.html', {'total_marked_units' : total_marked_units,
                                                       'total_unmarked_units' : total_unmarked_units,
                                                       'total_units' : total_units,
                                                       'marked_8' : marked_8,
                                                       'marked_4' : marked_4,
                                                       'marked_2' : marked_2})

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

    units_per_student = {}
    for student in all_students:
        counter =  MappingUnitToUser.objects.filter(already_marked=True, user=student)\
                                                 .count()
        units_per_student.update({student:counter})

    if request.user.is_superuser:
        return render(request, 'extractor/allstats.html', {'total_marked_units' : total_saved_units,
                                                           'total_unmarked_units' : total_unsaved_units,
                                                           'total_units' : total_units,
                                                           'all_distinct' : marked_units_distinct,
                                                           'all_students' : all_students,
                                                           'units_per_student' : units_per_student})

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

    length = len(unit_attributes[0]["plaintext"])
    if currentPos < length:
        unmarked_chars += length-currentPos

    percentage = round((unmarked_chars/length) * 100, 2)
    return unmarked_chars, percentage


def agreement(request, pk):
    calculate_agreement(request.user, pk)
    mapped_unit = MappingUnitToUser.objects.get(user=request.user, documentation_unit__pk=pk)
    try:
        results = Agreement.objects.get(Q(first=mapped_unit) | Q(second=mapped_unit))
    except Agreement.DoesNotExist:
        return HttpResponse("Can not find an agreement")

    return render(request, 'extractor/agreement.html', {'unit' : pk,
                                                        'first' : results.first.pk,
                                                        'second' : results.second.pk,
                                                        'percentage' : results.percentage_by_types})

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
                                                 user__groups__name='Students')
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
            .get(documentation_unit__pk=pk, user__groups__name='Students')
    else:
        #got more than two units
        return False

    try:
        mapped_unit = MappingUnitToUser.objects.get(documentation_unit__pk=pk,user=current_user )
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
    agree = 100-((round(errors(count_markings_me,count_markings_comp)/len(my_results),4))*100)

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