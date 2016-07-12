from django.shortcuts import render


class Middleware(object):

    def process_request(self, request):
        if request.path.startswith('/api/'):
            return

        UA = request.META.get('HTTP_USER_AGENT', '').lower()

        if 'trident' in UA or 'msie' in UA:
            return render(request, 'blockIE.html')
