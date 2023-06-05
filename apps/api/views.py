import json
import logging
import requests
from django.http import JsonResponse
from apps.thread.models import Thread, ThreadSession
from apps.thread.classes import ThreadWrapper

# Create your views here.
def push_data(request):
    """push data to external API"""
    key = request.GET.get('key')
    from_number = request.GET.get('from_number')
   
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})


def insurance_information(request):
    """Sample API for pull data """
    uuid = request.GET['uuid']

    wrapper = ThreadWrapper()
    request = wrapper.process_data(uuid= uuid)
    response = json.loads(request.content)
    print(response)

    #construct message
    message = "<b>HAKIKI TAARIFA</b> \n\n" \
    
    if 'Insurance_Taarifa' in response['arr_data']:
        message += "<b>Unatoa Taarifa kama: </b> " + response['arr_data']['Insurance_Taarifa'] + " \n"
        
    if 'Insurance_Phone' in response['arr_data']:
        message += "<b>Namba ya Simu:</b> " + response['arr_data']['Insurance_Phone'] + " \n" 

    if 'Insurance_Vehicle_No' in response['arr_data']:
        message += "<b>Namba ya usajili wa chombo:</b> " + response['arr_data']['Insurance_Vehicle_No'] + " \n" 

    if 'Insurance_Tarehe' in response['arr_data']:
        message += "<b>Tarehe Ya Ajali:</b> " + response['arr_data']['Insurance_Tarehe'] + " \n"  

    if 'Insurance_Time' in response['arr_data']:
        message += "<b>Muda wa Ajali:</b> " + response['arr_data']['Insurance_Time'] + " \n"  

    if 'Insurance_Driver_Licence' in response['arr_data']:
        message += "<b>Leseni ya Dereva:</b> " + response['arr_data']['Insurance_Driver_Licence'] + " \n"   

    if 'Insurance_Police_Office' in response['arr_data']:
        message += "<b>Jina la Kituo Cha Polisi:</b> " + response['arr_data']['Insurance_Police_Office'] + " \n" 
        
    if 'Insurance_Police_Reference' in response['arr_data']:
        message += "<b>Kumbukumbu Namba ya ajali:</b> " + response['arr_data']['Insurance_Police_Reference'] + " \n" 
    
    if 'Insurance_Accident_Reason' in response['arr_data']:
        message += "<b>Sababu ya ajali:</b> " + response['arr_data']['Insurance_Accident_Reason'] + " \n" 

    if 'Insurance_Damage_Other_Vehicle' in response['arr_data']:
        message += "<b>Uharibifu wa vyombo vingine:</b> " + response['arr_data']['Insurance_Damage_Other_Vehicle'] + " \n" 

    if 'Insurance_Accident_Vehicle' in response['arr_data']:
        message += "<b>Namba za usajili wa vyombo vingine :</b> " + response['arr_data']['Insurance_Accident_Vehicle'] + " \n" 

    if 'Insurance_Property_Damage' in response['arr_data']:
        message += "<b>Hasara kwa mali zingine:</b> " + response['arr_data']['Insurance_Property_Damage'] + " \n" 

    if 'Insurance_People_Damage' in response['arr_data']:
        message += "<b>Majeruhi kwa watu:</b> " + response['arr_data']['Insurance_People_Damage'] + " \n" 

    if 'Insurance_No_Casualties' in response['arr_data']:
        message += "<b>Idadi ya Majeruhi:</b> " + response['arr_data']['Insurance_No_Casualties'] + " \n" 

    message += "<b>Declaration (Tamko):</b> Mimi/Sisi nina/tunatoa tamko ya kwamba maelezo yaliyotolewa hapo juu pamoja na muhtasari wake ni ya ukweli na yamekamilika. Kama sivyo ni/tutawajibika kwa yatakayojiri."

    response = {
        "message": message,
        "arr_message": []
    }
     
    """response"""
    return JsonResponse({'status': 'success', 'response': response})

def loans(request):
    """Sample API for pull data """
    msisdn = request.GET['msisdn']

    response = {
        'msisdn': msisdn,
        "message": None,
        "arr_message": [
            {
                "id": "1",
                "message": "MC 123 (deni 45,000)",
                "description": ""
            },
            {
                "id": "2",
                "message": "MCCX77889 (deni 20,000)",
                "description": ""
            }
        ]
    }

        
    """response"""
    return JsonResponse({'status': 'success', 'response': response})


def repayments(request):
    """Sample API for pull data """
    msisdn = request.GET['msisdn']

    response = {
        'msisdn': msisdn,
        "message": None,
        "arr_message": [
            {
                "id": "1",
                "message": "MC 123 (deni 45,000)",
                "description": ""
            },
            {
                "id": "2",
                "message": "MCCX77889 (deni 20,000)",
                "description": ""
            }
        ]
    }
   
    """response"""
    return JsonResponse({'status': 'success', 'response': response})


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
