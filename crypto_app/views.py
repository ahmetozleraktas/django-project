from datetime import datetime
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import requests
from .models import Crypto
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

_BASE_SYMBOL = 'USDT'
_API_KEY = '2fays/HuwDMPf6MDKchcTA==A0PchcFQX0LOAmQb'

@api_view(['POST', 'GET'])  # Specify the HTTP methods supported
@renderer_classes([JSONRenderer])  # Specify the renderers you want here
def index(request):
    return Response({'foo':'bar'})

    
@api_view(['POST', 'GET'])  # Specify the HTTP methods supported
@renderer_classes([JSONRenderer])  # Specify the renderers you want here
def price(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol', None)
        if symbol is None:
            return Response({'result':'NEED SYMBOL TO CREATE COLLECTION TASK.'})
        else:
            # add periodic task to django_celery_beat
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=10,
                period=IntervalSchedule.SECONDS,
            )
            task, created = PeriodicTask.objects.get_or_create(
                interval=schedule,
                name=f'get_price_{symbol}',
                task='crypto_app.views.get_price',
                args=json.dumps([symbol]),
                kwargs=json.dumps({}),
            )
            return Response({'result':'PERIODIC TASK ADDED.'})
        

@api_view(['POST', 'GET'])  # Specify the HTTP methods supported
@renderer_classes([JSONRenderer])  # Specify the renderers you want here
def show_price(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol', None)
        if symbol is None:
            return Response({'result':'NEED SYMBOL TO GET PRICE.'})
        else:
            try:
                crypto = Crypto.objects.get(symbol=symbol)
                return Response({'result':crypto.price})
            except Crypto.DoesNotExist:
                return Response({'result':'NO PRICE FOUND.'})
            