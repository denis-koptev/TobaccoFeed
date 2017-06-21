from django.shortcuts import render

def user(request):
	return render(request, 'user_page/user_page.html', {})