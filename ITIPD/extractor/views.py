from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
import datetime
from django.views import generic
from extractor.models import DocumentationUnit, KnowledgeType, MarkedUnit, ParentElement
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login


def testing(request, *number):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class DetailView(generic.DetailView):
    model = DocumentationUnit
    template_name = 'extractor/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context

# data: JSON.stringify(data_to_send)
# data: { data: JSON.stringify(data_to_send)}


class ParentView(generic.DeleteView):
    model = ParentElement
    template_name = 'extractor/parents.html'

    def get_context_data(self, **kwargs):
        context = super(ParentView, self).get_context_data(**kwargs)
        return context

@csrf_exempt
#@login_required
def vote(request):
    if request.method != 'POST':
        data = {'error': 'Invalid method'}
        return HttpResponseBadRequest(
            json.dumps(data), content_type='application/json'
        )

    #data = json.loads(request.POST['data'])
    documentation_id = json.loads(request.POST['unit'])
    documentation_unit1 = DocumentationUnit.objects.get(pk=documentation_id)
    getrange = json.loads(request.POST['range'])
    html = request.POST['html_text']

    for entry in getrange:
        marked_unit = MarkedUnit.objects.create(
            user=request.user,
            documentation_unit=documentation_unit1,
            knowledge_type=entry['type'],
            html_text=html,
            range=entry['serializedRange']
        )

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
            # TODO Redirect to a success page.
        else:
            print("disabled account")
            # TODO Return a 'disabled account' error message
    else:
        print("invalid login")
         # TODO Return an 'invalid login' error message.
