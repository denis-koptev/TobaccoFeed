from django import template
from django.template.defaultfilters import stringfilter
from tobaccopoisk import utils
from tobacco_page.models import Tobacco

register = template.Library()

@register.filter
@stringfilter
def real_url(s):
    return utils.image_url_handler(s)

#@register.filter
#def real_param(tobacco, param):
#	return tobacco.get_param(param)

@register.filter(name='realVote')
def realVote(uto, arg):
	if uto == None:
		return 0
	if arg == "strength":
		return uto.strength_vote
	elif arg == "smoke":
		return uto.smoke_vote
	elif arg == "heat":
		return uto.heat_vote
	elif arg == "taste":
		return uto.taste_vote
	elif arg == "rating":
		return uto.rating_vote
	else:
		return 0

@register.filter(name='realParam')
def realParam(tobacco, param):
	if tobacco == None:
		return 0
	if param == 'heat':
		return tobacco.heat
	elif param == 'taste':
		return tobacco.taste
	elif param == 'smoke':
		return tobacco.smoke
	elif param == 'strength':
		return tobacco.strength
	elif param == 'rating':
		return tobacco.rating
	else:
		return 0

@register.filter(name='realParamAmount')
def realParamAmount(tobacco, param):
	if tobacco == None:
		return 0
	if param == 'heat':
		return tobacco.heat_votes
	elif param == 'taste':
		return tobacco.taste_votes
	elif param == 'smoke':
		return tobacco.smoke_votes
	elif param == 'strength':
		return tobacco.strength_votes
	elif param == 'rating':
		return tobacco.rating_votes
	else:
		return 0
