from django.shortcuts import render
from tobacco_page.models import Tobacco
from search_page.engine import to_dict

def get_last(count):
	try:
		last = Tobacco.objects.all().order_by("-id").values_list('brand', 'name', 'image')[:count]

	except Tobacco.DoesNotExist:
		return []
	return [to_dict(rec) for rec in last]

def main(request):
	context = {'latest' : get_last(5)}
	return render(request, 'main_page/main_page.html', context)