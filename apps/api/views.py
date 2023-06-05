import json
import logging
import requests
from django.http import HttpResponse, JsonResponse

# Create your views here.
def push_data(request):
    """push data to external API"""
    key = request.GET.get('key')
    from_number = request.GET.get('from_number')
   
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})


def loans(request):
    """Sample API for pull data """
    msisdn = request.GET['msisdn']

    loans = {
        'msisdn': msisdn,
        loans: [
            {
                "id": 1,
                "message": "MC 123 (deni 45,000)",
            },
            {
                "id": 2,
                "message": "MCCX77889 (deni 20,000)",
            }
        ]
    }

        
    """response"""
    return JsonResponse({'status': 'success', 'response': loans})


def pull(request):
    """Sample API for pull data """
    msg = request.GET['msg']
    sessionId = request.GET['sessionId']
    msisdn = request.GET['msisdn']

    print(msg)
    print(msisdn)
    print(sessionId)

    message = "Hello Renfrid, Tafathali chagua huduma zifuatazo\n" \
                "1. Ngao ya buku\n" \
                "2. BimaPap\n" \
                "3. Huduma kwa wateja\n" \

        
    """response"""
    return JsonResponse({'status': 'success', 'message': message})
