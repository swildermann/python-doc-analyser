from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
import datetime, random, ast
from extractor.models import DocumentationUnit, KnowledgeType, MarkedUnit, MappingUnitToUser, AccessLog
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.db.models import Count


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
    unit_list = (MappingUnitToUser.objects.filter(user=request.user, already_marked=False)\
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
    unit = DocumentationUnit.objects.get(pk=1544)
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

    return render (request, 'extractor/mystats.html', {'total_marked_units' : total_marked_units,
                                                       'total_unmarked_units' : total_unmarked_units,
                                                       'total_units' : total_units})

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

    percentage = round(unmarked_chars/length * 100, 2)
    return (unmarked_chars, percentage)


def agreement(request, pk):
    try:
        doc_unit = DocumentationUnit.objects.get(id=pk)
        mapped_unit = MappingUnitToUser.objects.get(documentation_unit__pk=pk,user=request.user)
        marked_unit = MarkedUnit.objects.filter(documentation_unit__pk=pk,user=request.user).count()
        marked_unit_of_others = MarkedUnit.objects.exclude(user=request.user).filter(documentation_unit__pk=pk)\
            .count()
        how_many = MarkedUnit.objects.exclude(user=request.user).filter(documentation_unit__pk=pk)\
            .distinct('user').count()

    except MappingUnitToUser.DoesNotExist:
        return HttpResponse("This unit is not mapped.")

    data = []
    for each in mapped_unit:
        ids = each["id"]
        start= ast.literal_eval(each["char_range"])[0]["characterRange"]["start"]
        end= ast.literal_eval(each["char_range"])[0]["characterRange"]["end"]
        data.append((ids,start,end))
    data.sort(key=lambda tup: tup[1])
    #TODO merge beneath markings!


    return render(request, 'extractor/agreement.html', {'unit' : mapped_unit,
                                                        'doc_unit': doc_unit,
                                                        'marked_unit' : marked_unit,
                                                        'marked_unit2' : marked_unit_of_others,
                                                        'how_many' : how_many})