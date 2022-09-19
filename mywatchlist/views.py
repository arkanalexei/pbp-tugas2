from django.shortcuts import render
from mywatchlist.models import MyWatchList
from django.http import HttpResponse
from django.core import serializers
# Create your views here.

def show_mywatchlist(request):
    return render(request, "mywatchlist.html", context)
    
def show_xml(request):
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = MyWatchList.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = MyWatchList.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


data = MyWatchList.objects.all()
context = {
    "list_movie_item": data,
    "num_watched": MyWatchList.objects.filter(watched=True).count(),
    "num_not_watched": MyWatchList.objects.filter(watched=False).count(),
}
