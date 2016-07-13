from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')


def redirect_view(request):
    return redirect('/#%s?%s' % (
        request.path,
        request.META.get('QUERY_STRING', '')
    ))
