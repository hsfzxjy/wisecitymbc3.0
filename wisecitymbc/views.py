from rest_framework.response import Response
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

def login(request):
	return render_to_response('login.html')
def index(request):
	return render_to_response('index.html')
def articles(request):
	return render_to_response('articles.html')