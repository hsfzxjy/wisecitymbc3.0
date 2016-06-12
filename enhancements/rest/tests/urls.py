from django.conf.urls import url, include

from enhancements.rest.urls import generate_urls

urlpatterns = [
    url('^', include(generate_urls()))
]
