import json
import logging
import requests
from django.http import JsonResponse
from apps.thread.models import Thread, ThreadSession
from apps.thread.classes import ThreadWrapper
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def insurance_information(request):
    """Sample API for pull data """
    if request.method == "POST":
        uuid = request.POST['uuid']
        logging.info(uuid)

        wrapper = ThreadWrapper()
        request = wrapper.process_data(uuid=uuid)
        response = json.loads(request.content)

        if response['status'] == 'success':
            #construct message
            message = "*_Hakiki Taarifa za madai ya BIMA_* \n\n" \
            
            if 'Taarifa' in response['arr_data']:
                message += "*Unatoa Taarifa kama:* " + response['arr_data']['Taarifa'] + " \r\n"
                
            if 'Phone' in response['arr_data']:
                message += "*Namba ya Simu:* " + response['arr_data']['Phone'] + " \r\n" 

            if 'Vehicle_Number' in response['arr_data']:
                message += "*Namba ya usajili wa chombo:* " + response['arr_data']['Vehicle_Number'] + " \r\n" 

            if 'Insurance_Type' in response['arr_data']:
                message += "*Aina ya Madai:* " + response['arr_data']['Insurance_Type'] + " \r\n"  

            if 'Accident_Date' in response['arr_data']:
                message += "*Tarehe Ya Ajali:* " + response['arr_data']['Accident_Date'] + " \r\n"  

            if 'Theft_Date' in response['arr_data']:
                message += "*Tarehe Ya Wizi:* " + response['arr_data']['Theft_Date'] + " \r\n"  

            if 'Accident_Time' in response['arr_data']:
                message += "*Muda wa Ajali:* " + response['arr_data']['Accident_Time'] + " \r\n"  

            if 'Theft_Time' in response['arr_data']:
                message += "*Muda wa Wizi:* " + response['arr_data']['Theft_Time'] + " \r\n"  

            if 'Accident_Location' in response['arr_data']:
                message += "*Sehemu/Mahali:* " + response['arr_data']['Accident_Location'] + " \r\n"  

            if 'Theft_Location' in response['arr_data']:
                message += "*Sehemu/Mahali:* " + response['arr_data']['Theft_Location'] + " \r\n" 

            if 'Driver_Licence' in response['arr_data']:
                message += "*Leseni ya Dereva:* " + response['arr_data']['Driver_Licence'] + " \r\n"   

            if 'Police_Station' in response['arr_data']:
                message += "*Jina la Kituo Cha Polisi:* " + response['arr_data']['Police_Station'] + " \r\n" 
                
            if 'Police_RB' in response['arr_data']:
                message += "*Kumbukumbu Namba(RB):* " + response['arr_data']['Police_RB'] + " \r\n" 
            
            if 'Accident_Reason' in response['arr_data']:
                message += "*Sababu ya ajali:* " + response['arr_data']['Accident_Reason'] + " \r\n" 

            if 'Vehicle_Damage' in response['arr_data']:
                message += "*Madhara kwenye chombo:* " + response['arr_data']['Vehicle_Damage'] + " \r\n"      

            if 'Other_Vehicle_Damage' in response['arr_data']:
                message += "*Uharibifu wa vyombo vingine:* " + response['arr_data']['Other_Vehicle_Damage'] + " \r\n" 

            if 'Other_Vehicle_Damage_Registration' in response['arr_data']:
                message += "*Namba za usajili wa vyombo vingine :* " + response['arr_data']['Other_Vehicle_Damage_Registration'] + " \r\n" 

            if 'Property_Damage' in response['arr_data']:
                message += "*Hasara kwa mali zingine:* " + response['arr_data']['Property_Damage'] + " \r\n" 

            if 'Property_Theft' in response['arr_data']:
                message += "*Je vitu vimeibiwa?:* " + response['arr_data']['Property_Theft'] + " \r\n" 

            if 'Property_Theft_Info' in response['arr_data']:
                message += "*Vitu vilivyoibiwa:* " + response['arr_data']['Property_Theft_Info'] + " \r\n" 

            if 'People_Damage' in response['arr_data']:
                message += "*Majeruhi kwa watu:* " + response['arr_data']['People_Damage'] + " \r\n" 

            if 'Number_of_Casualties' in response['arr_data']:
                message += "*Idadi ya Majeruhi:* " + response['arr_data']['Number_of_Casualties'] + " \r\n" 

            Full_Name = ""
            if 'Full_Name' in response['arr_data']:
                Full_Name = response['arr_data']['Full_Name']

            message += f"\r\n\n*Declaration (Tamko):* Mimi *{Full_Name}*, ninakiri kwamba maelezo yaliyotolewa hapo juu pamoja na muhtasari wake ni sahihi na ya ukweli na yamekamilika. Kama sivyo nitawajibika ipasavyo."
        
        elif response['status'] == 'failed':
            message = response['error_msg'] 

        """response"""
        return JsonResponse({"message": message, "arr_message": []})

        

