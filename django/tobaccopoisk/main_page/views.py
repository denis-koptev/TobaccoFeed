from django.shortcuts import render

def main(request):
    return render(request, 'main_page/main_page.html', {})