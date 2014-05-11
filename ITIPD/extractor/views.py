from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
import datetime
from django.views import generic
from extractor.models import DocumentationUnit, KnowledgeType, MarkedUnit, MappingUnitToUser
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class DetailView(generic.DetailView):
    model = DocumentationUnit
    template_name = 'extractor/display_unit.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context


class ParentView(generic.DeleteView):
    model = DocumentationUnit
    template_name = 'extractor/parents.html'

    def get_context_data(self, **kwargs):
        context = super(ParentView, self).get_context_data(**kwargs)
        return context


class FileView(generic.DeleteView):
    model = DocumentationUnit
    template_name = 'extractor/display_file.html'

    def get_context_data(self, **kwargs):
        context = super(FileView, self).get_context_data(**kwargs)
        return context


@csrf_exempt
@login_required(login_url='/login/')
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
    for entry in getrange:
        marked_unit = MarkedUnit.objects.create(
            user=current_user,
            documentation_unit=documentation_unit1,
            knowledge_type=entry['type'],
            html_text=html,
            range=entry['serializedRange'],
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
@login_required(login_url='/login/')
def show_next_unit(request):
    unit_list = (MappingUnitToUser.objects.filter(user=request.user)).filter(already_marked=False).order_by('id')
    if len(unit_list) == 0:
        return render(request, 'extractor/no_units.html')
    unit = unit_list[0]
    return render(request, 'extractor/detail.html', {'object' : unit.documentation_unit})