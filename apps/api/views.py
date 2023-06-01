import json
import logging
import requests
from django.http import HttpResponse, JsonResponse

# Create your views here.
def push_data(request):
    """push data to external API"""
    key = request.GET.get('key')
    from_number = request.GET.get('from_number')

    arr_data = {

    }


        
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})


def pull(request):
    """Sample API for pull data """
    key = request.GET.get('message')
    from_number = request.GET.get('from_number')

    print(key)
    print(from_number)

    message = "Hello Renfrid, Tafathali chagua huduma zifuatazo\n" \
                "1. Ngao ya buku\n" \
                "2. BimaPap\n" \
                "3. Huduma kwa wateja\n" \

        
    """response"""
    return JsonResponse({'status': 'success', 'message': message})
