from tobacco_page.models import Tobacco
from tobaccopoisk import utils
import math

def to_dict(inst):
	return 	{
			'brand': utils.to_view_str(inst[0]),
			'name': utils.to_view_str(inst[1]),
			'url': "/" + inst[0] + "/" + inst[1],
			'image': utils.image_url_handler(inst[2]),
			}


def max_substr(a, b):
	if (a == b):
		return a

	if (len(a) == 0 or len(b) == 0):
		return ""

	matrix = [[0 for x in b] for y in a]

	max_length = 0
	max_idx = 0

	for i in range(len(a)) :
		for j in range(len(b)) :
			if a[i] == b[j] :
				if i != 0 and j != 0 :
					matrix[i][j] = matrix[i-1][j-1] + 1
				else:
					matrix[i][j] = 1
				if matrix[i][j] > max_length :
					max_length = matrix[i][j]
					max_idx = i
	return a[max_idx - max_length + 1 : max_idx + 1]


def search(q):

	try:
		insts = Tobacco.objects.values_list('brand', 'name', 'image')
	except Tobacco.DoesNotExist:
		return []

	q = utils.to_search_str(q)
	if len(q) == 0:
		return []

	data = [to_dict(inst) for inst in insts]

	if q == "<all>":
		return data

	# SEARCH CODE STARTED

	filtered = []

	for item in data:

		ident = item["brand"] + item["name"]
		ident = utils.to_search_str(ident)
		len_ident = len(ident)

		loc_q = q
		max_sub = max_substr(loc_q, ident)
		coeff = 0

		while len(max_sub) > 1:
			loc_q = loc_q.replace(max_sub, " ")
			#coeff = coeff + len(max_sub) #*len(max_sub)
			coeff = coeff + (1.4**len(max_sub) / 1.4**len(q))
			max_sub = max_substr(loc_q, ident)

		print(q + " " + ident + " " + str(coeff))

		if coeff / len_ident == 1:
			return [item]

		if coeff >= 0.3:
			item["coeff"] = coeff
			filtered.append(item)

	filtered = sorted(filtered, key=lambda k: k['coeff'], reverse = True)

	return filtered
	