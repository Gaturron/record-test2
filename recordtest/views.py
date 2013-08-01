# Imports
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

##
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
def error404(request):

    # 1. Load models for this view
    #from idgsupply.models import My404Method

    # 2. Generate Content for this view
    t = loader.get_template('404.html')

    # 3. Return Template for this view + Data
    return HttpResponse(content=t.render(Context({})), content_type='text/html; charset=utf-8', status=404)