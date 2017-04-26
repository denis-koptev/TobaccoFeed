from tobacco.models import Tobacco

def image_url_handler(url):
	idx = url.find('/static/')
	return url[idx:]

def to_dict(inst):
	return 	{
			'brand': inst[0],
			'name': inst[1],
			'image': image_url_handler(inst[2]),
			}

def max_substr(a, b):
	lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
	for i, x in enumerate(a):
	    for j, y in enumerate(b):
	        if x == y:
	            lengths[i+1][j+1] = lengths[i][j] + 1
	        else:
	            lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
	return lengths[len(a)][len(b)]

def search(q):
	try:
		insts = Tobacco.objects.values_list('brand', 'name', 'image')
	except Tobacco.DoesNotExist:
		return []

	q = q.replace(' ', '').replace('-', '').replace('_', '').lower()

	data = [to_dict(inst) for inst in insts]

	# SEARCH CODE STARTED

	filtered = []

	for item in data:

		ident = item["brand"] + item["name"]
		ident = ident.replace(' ', '').replace('-', '').replace('_', '')
		len_ident = len(ident)

		coeff = max_substr(q, ident)

		if coeff / len_ident == 1:
			return [item]

		if coeff / len(q) >= 0.9:
			item["coeff"] = coeff
			filtered.append(item)

	filtered = sorted(filtered, key=lambda k: k['coeff'], reverse = True)

	return filtered