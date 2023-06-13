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
    message = "*_Hakiki Taarifa za madai ya BIMA_* \n\n" \
    
    if 'Taarifa' in response['arr_data']:
        message += "*Unatoa Taarifa kama:* " + response['arr_data']['Taarifa'] + " \n"
        
    if 'Phone' in response['arr_data']:
        message += "*Namba ya Simu:* " + response['arr_data']['Phone'] + " \n" 

    if 'Vehicle_Number' in response['arr_data']:
        message += "*Namba ya usajili wa chombo:* " + response['arr_data']['Vehicle_Number'] + " \n" 

    if 'Insurance_Type' in response['arr_data']:
        message += "*Aina ya Madai:* " + response['arr_data']['Insurance_Type'] + " \n"  

    if 'Accident_Date' in response['arr_data']:
        message += "*Tarehe Ya Ajali:* " + response['arr_data']['Accident_Date'] + " \n"  

    if 'Theft_Date' in response['arr_data']:
        message += "*Tarehe Ya Wizi:* " + response['arr_data']['Theft_Date'] + " \n"  

    if 'Accident_Time' in response['arr_data']:
        message += "*Muda wa Ajali:* " + response['arr_data']['Accident_Time'] + " \n"  

    if 'Theft_Time' in response['arr_data']:
        message += "*Muda wa Wizi:* " + response['arr_data']['Theft_Time'] + " \n"  

    if 'Accident_Location' in response['arr_data']:
        message += "*Sehemu/Mahali:* " + response['arr_data']['Accident_Location'] + " \n"  

    if 'Theft_Location' in response['arr_data']:
        message += "*Sehemu/Mahali:* " + response['arr_data']['Theft_Location'] + " \n" 

    if 'Driver_Licence' in response['arr_data']:
        message += "*Leseni ya Dereva:* " + response['arr_data']['Driver_Licence'] + " \n"   

    if 'Police_Station' in response['arr_data']:
        message += "*Jina la Kituo Cha Polisi:* " + response['arr_data']['Police_Station'] + " \n" 
        
    if 'Police_RB' in response['arr_data']:
        message += "*Kumbukumbu Namba(RB):* " + response['arr_data']['Police_RB'] + " \n" 
    
    if 'Accident_Reason' in response['arr_data']:
        message += "*Sababu ya ajali:* " + response['arr_data']['Accident_Reason'] + " \n" 

    if 'Vehicle_Damage' in response['arr_data']:
        message += "*Madhara kwenye chombo:* " + response['arr_data']['Vehicle_Damage'] + " \n"      

    if 'Other_Vehicle_Damage' in response['arr_data']:
        message += "*Uharibifu wa vyombo vingine:* " + response['arr_data']['Other_Vehicle_Damage'] + " \n" 

    if 'Other_Vehicle_Damage_Registration' in response['arr_data']:
        message += "*Namba za usajili wa vyombo vingine :* " + response['arr_data']['Other_Vehicle_Damage_Registration'] + " \n" 

    if 'Property_Damage' in response['arr_data']:
        message += "*Hasara kwa mali zingine:* " + response['arr_data']['Property_Damage'] + " \n" 

    if 'Property_Theft' in response['arr_data']:
        message += "*Je vitu vimeibiwa?:* " + response['arr_data']['Property_Theft'] + " \n" 

    if 'Property_Theft_Info' in response['arr_data']:
        message += "*Vitu vilivyoibiwa:* " + response['arr_data']['Property_Theft_Info'] + " \n" 

    if 'People_Damage' in response['arr_data']:
        message += "*Majeruhi kwa watu:* " + response['arr_data']['People_Damage'] + " \n" 

    if 'Number_of_Casualties' in response['arr_data']:
        message += "*Idadi ya Majeruhi:* " + response['arr_data']['Number_of_Casualties'] + " \n\n\n\n" 

    message += "*Declaration (Tamko):* Mimi/Sisi nina/tunatoa tamko ya kwamba maelezo yaliyotolewa hapo juu pamoja na muhtasari wake ni ya ukweli na yamekamilika. Kama sivyo ni/tutawajibika kwa yatakayojiri."
     
    """response"""
    return JsonResponse({"message": message, "arr_message": []})

