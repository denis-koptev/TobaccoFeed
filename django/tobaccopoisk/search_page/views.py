import json
from django.http import HttpResponse
from tobacco.models import Tobacco

def image_url_handler(url):
	idx = url.find('/static/')
	return url[idx:]

def search(request):
	
	def to_dict(inst):
		return 	{
				'brand': inst[0],
				'name': inst[1],
				'image': image_url_handler(inst[2]),
				}

	try:
		insts = Tobacco.objects.values_list('brand', 'name', 'image')
	except Tobacco.DoesNotExist:
		return HttpResponse("{}".format(json.dumps({"data": []}, ensure_ascii=False)))

	q = request.GET.get('q')
	data = [to_dict(inst) for inst in insts]

	return HttpResponse("{}".format(json.dumps({"data": data}, ensure_ascii=False)))