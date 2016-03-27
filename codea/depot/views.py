# general imports
import datetime, json, sys, pytz

# django imports
from django.shortcuts import *
from django.template import RequestContext
from django.http import JsonResponse

# main view for depot
def depot(request):
        context = {}
        return render(request, 'depot/depot.html', context)
