from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
import datetime
from django.views import generic
from extractor.models import DocumentationUnit, KnowledgeType, MarkedUnit
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson



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



@csrf_exempt
#@login_required
def vote(request):
    if request.method != 'POST':
        data = {'error': 'Invalid method'}
        return HttpResponseBadRequest(
            json.dumps(data), content_type='application/json'
        )

    data = json.loads(request.POST['data'])
    documentation_id = json.loads(request.POST['unit'])
    documentation_unit1=DocumentationUnit.objects.get(pk=documentation_id)

    for entry in data:
        marked_unit = MarkedUnit.objects.create(
            user=request.user,
            documentation_unit=documentation_unit1,
            knowledge_type=entry['type_id'],
            html_text=entry['selected_text']
        )

    return HttpResponse(
        json.dumps({'success': request.POST['data']}),
        content_type='application/json'
    )



