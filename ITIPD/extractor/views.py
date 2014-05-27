from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
import datetime, random
from extractor.models import DocumentationUnit, KnowledgeType, MarkedUnit, MappingUnitToUser, AccessLog
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count


def view_unit(request, pk):
    documentation_id = pk
    try:
        documentation_unit1 = DocumentationUnit.objects.get(id=documentation_id)
    except DocumentationUnit.DoesNotExist:
        raise Http404
    current_user = request.user
    now = datetime.datetime.now()

    access_log = AccessLog.objects.create(
            user=current_user,
            documentation_unit=documentation_unit1,
            timestamp=now,
            filename = "view_unit")

    marked_units = (MarkedUnit.objects.filter(user=request.user, documentation_unit=documentation_unit1))

    return render(request, 'extractor/display_unit.html', {'object': documentation_unit1, 'marked_units': marked_units})


def show_parent(request, pk):
    documentation_id = pk
    try:
        documentation_unit1 = DocumentationUnit.objects.get(id=documentation_id)
    except DocumentationUnit.DoesNotExist:
        raise Http404
    current_user = request.user
    now = datetime.datetime.now()

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
    now = datetime.datetime.now()

    access_log = AccessLog.objects.create(
            user=current_user,
            documentation_unit=documentation_unit1,
            timestamp=now,
            filename = "file")

    return render(request, 'extractor/display_file.html', {'object': documentation_unit1})


@csrf_exempt
@login_required(login_url='/extractor/login/')
def vote(request):
    if request.method != 'POST':
        data = {'error': 'Invalid method'}
        return HttpResponseBadRequest(
            json.dumps(data), content_type='application/json'
        )

    now = datetime.datetime.now()
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
    unit_list = (MappingUnitToUser.objects.filter(user=request.user))\
                .filter(already_marked=False).order_by('documentation_unit')
    current_user = request.user
    if len(unit_list) == 0:
        return render(request, 'extractor/no_units.html')
    unit = unit_list[0]
    print(unit.id)
    now = datetime.datetime.now()
    store_unit = DocumentationUnit.objects.get(pk = unit.documentation_unit.id)
    access_log = AccessLog.objects.create(
        user=current_user,
        documentation_unit=store_unit,
        timestamp=now,
        filename="rate_unit")

    return render(request, 'extractor/detail.html', {'object': unit.documentation_unit})

@login_required(login_url='')
def marked_units(request):
    units = DocumentationUnit.objects.filter(mappingunittouser__user__pk__exact=request.user.pk)\
                                     .filter(mappingunittouser__already_marked__exact=True)\
                                     .annotate(num_markings = Count('markedunit')).order_by('id')
    return render(request, 'extractor/markedunits.html', {'units': units})


@login_required(login_url='')
def random_mapping(request):
    number = random.randint(1, 8300)
    current_user = request.user
    unit = DocumentationUnit.objects.get(pk=number)
    if current_user.is_superuser:
        mapUnitToUser = MappingUnitToUser.objects.create(
            user=current_user,
            documentation_unit=unit,
            already_marked=False
        )
        return render(request, 'extractor/randomunit.html')
    return HttpResponse("You need to be superuser for that..!") 

def mystats(request):
    total_marked_units = DocumentationUnit.objects.filter(mappingunittouser__user__pk__exact=request.user.pk)\
                                     .filter(mappingunittouser__already_marked__exact=True)\
                                     .count()
    total_unmarked_units = DocumentationUnit.objects.filter(mappingunittouser__user__pk__exact=request.user.pk)\
                                     .filter(mappingunittouser__already_marked__exact=False)\
                                     .count()
    total_units = total_marked_units + total_unmarked_units

    return render (request, 'extractor/mystats.html', {'total_marked_units' : total_marked_units,
                                                       'total_unmarked_units' : total_unmarked_units,
                                                       'total_units' : total_units})
def allstats(request):
    total_marked_units = DocumentationUnit.objects.filter(mappingunittouser__already_marked__exact=True)\
                                     .count()
    total_unmarked_units = DocumentationUnit.objects.filter(mappingunittouser__already_marked__exact=False)\
                                     .count()
    total_units = total_marked_units + total_unmarked_units

    if request.user.is_superuser:
        return render(request, 'extractor/allstats.html', {'total_marked_units' : total_marked_units,
                                                           'total_unmarked_units' : total_unmarked_units,
                                                           'total_units' : total_units})

    return HttpResponse("You need to be superuser for that..!")