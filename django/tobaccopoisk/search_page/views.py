import json
from django.http import HttpResponse
from tobacco.models import Tobacco
from django.shortcuts import redirect
from .engine import search as do_search

def search(request):
	q = request.GET.get('q')
	
	filtered = do_search(q)

	if len(filtered) == 1:
		return redirect("/" + filtered[0]["brand"].lower().replace(' ', '_') + "/" + filtered[0]["name"].lower().replace(' ', '_'))

	return HttpResponse("{}".format(json.dumps({"data": filtered}, ensure_ascii=False)))