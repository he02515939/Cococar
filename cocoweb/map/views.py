# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Marker


# Create your views here.
def home(request):
    return render(request, "map.html")


def about(request):
    return render(request, "about.html")


def search_record(request):
    pass


@csrf_exempt
def request_marker(request):
    if request.method == "POST":
        rc = json.loads(request.body)
        marker_id = rc.get("marker_id")
        if marker_id is None:
            return HttpResponse(status=400)
        if "live_finish" in rc.keys():
            try:
                marker = Marker.objects.get(marker_id=marker_id)
            except Marker.DoesNotExist:
                return HttpResponse(status=400)
            marker.live_ending_time = datetime.datetime.now()
            marker.save()
            return HttpResponse(status=200)
        else:
            marker_id = rc.get("marker_id")
            marker = Marker.objects.get_or_create(marker_id=marker_id)[0]
            print(marker)
            for key in rc.keys():
                setattr(marker, key, rc[key])
            marker.save()
            return HttpResponse(status=200)
    else:
        queryset = Marker.objects.filter(marker_id__istartswith="marker") \
                                 .filter(create__gte=timezone.now() - datetime.timedelta(hours=1))
        queryset2 = Marker.objects.filter(marker_id__istartswith="user")\
                                     .exclude(live_ending_time__isnull=False)
        response = dict()
        for q in [queryset, queryset2]:
            for m in q:
                d = {
                    "marker_id": m.marker_id,
                    "user_id": m.user_id,
                    "longitude": m.longitude,
                    "latitude": m.latitude,
                    "url": m.url,
                    "talk": m.talk,
                }
                response.update(d)
        return JsonResponse(data=response)



