from tobacco_page.models import Tobacco, Mix
from user_page.models import UserTobacco, UserMix
from django.db import DatabaseError

def recalc_tobacco_votes():
	params = ['strength', 'smoke', 'taste', 'heat', 'rating']

	# super query
	tobaccos = Tobacco.objects.prefetch_related('usertobacco_set').all()
	
	# recalculate votes for every tobacco
	for t in tobaccos:

		new_params = {}

		# zero all
		for p in params:
			new_params[p] = 0
			new_params[p + '_votes'] = 0

		# calc votes of users from utos
		for uto in t.usertobacco_set.all():
			for p in params:
				vote = getattr(uto, p + '_vote')
				if vote is not None:
					new_params[p] += vote
					new_params[p + '_votes'] += 1

		# summaty_vote / amount_of_votes
		for p in params:
			if new_params[p + '_votes'] != 0:
				setattr(t, p, new_params[p] / new_params[p + '_votes'])
				setattr(t, p + '_votes', new_params[p + '_votes'])

		try:
			t.save()
		except DatabaseError:
			print(str(t) + ' save error')

def recalc_mix_votes():
	# super query
	mixes = Mix.objects.prefetch_related('usermix_set').all()
	
	# recalculate votes for every tobacco
	for m in mixes:

		# zero all
		new_rating = new_rating_votes = 0

		# calc votes of users from utos
		for umo in m.usermix_set.all():
			if umo.rating_vote is not None:
				new_rating += umo.rating_vote
				new_rating_votes += 1

		# summaty_vote / amount_of_votes
		if new_rating_votes != 0:
			m.rating = new_rating / new_rating_votes
			m.rating_votes = new_rating_votes

		try:
			m.save()
		except DatabaseError:
			print(str(m) + ' save error')