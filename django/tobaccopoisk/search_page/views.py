import json
from django.http import HttpResponse
from tobacco.models import Tobacco
from tobacco.views import tobacco_view
from django.shortcuts import redirect

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
	q = q.replace(' ', '').replace('-', '').replace('_', '')

	data = [to_dict(inst) for inst in insts]

	# PIZDATIY CODE STARTED

	filtered = []

	for item in data:

		ident = item["brand"] + item["name"]
		ident = ident.replace(' ', '').replace('-', '').replace('_', '')
		len_ident = len(ident)

		loc_q = q

		eqs = 0
		for letter in loc_q:
			idx = ident.find(letter)
			if idx != -1:
				ident = ident[:idx] + ident[idx+1:]
				q_idx = loc_q.find(letter)
				loc_q = loc_q[:q_idx] + loc_q[q_idx+1:]
				eqs = eqs + 1

		# SUKAAAA ETO TAKOOOY PIZDATYI REDIRECT!!!! YA KON4IL!!!
		if eqs / len_ident == 1:
			return redirect("/" + item["brand"].lower().replace(' ', '_') + "/" + item["name"].lower().replace(' ', '_'))
			#return redirect("/afzal/pan-raas")

		# Else make filtration using coefficient calculated with user string
		if eqs / len(q) >= 0.7:
			item["coeff"] = eqs / len(q)
			filtered.append(item)

			print(item["brand"] + ' ' + item["name"] + ' ' + ident + ' ' + str(eqs))

		filtered = sorted(filtered, key=lambda k: k['coeff'], reverse = True)

	return HttpResponse("{}".format(json.dumps({"data": filtered}, ensure_ascii=False)))