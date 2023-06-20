import json
import logging
import requests
from django.http import JsonResponse
from apps.thread.models import Thread, ThreadSession
from apps.thread.classes import ThreadWrapper
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def rumor_information(request):
    """Sample API for pull data """
    if request.method == "POST":
        uuid = request.POST['uuid']
        logging.info(uuid)

        wrapper = ThreadWrapper()
        request = wrapper.process_data(uuid=uuid)
        response = json.loads(request.content)

        if response['status'] == 'success':
            #construct message
            message = "*_Hakiki Taarifa _* \n\n" \
            
            if 'Text' in response['arr_data']:
                message += "*Maelezo ya Tukio:* " + response['arr_data']['Text'] + " \r\n"
                
            if 'Village' in response['arr_data']:
                message += "*Kijiji/Mtaa:* " + response['arr_data']['Village'] + " \r\n" 

            if 'Ward' in response['arr_data']:
                message += "*Kata:* " + response['arr_data']['Ward'] + " \r\n" 

            if 'Rumor_Date' in response['arr_data']:
                message += "*Tarehe ya Tukio:* " + response['arr_data']['Rumor_Date'] + " \r\n"  

            if 'Street' in response['arr_data']:
                message += "*Jina Maarufu la Eneo:* " + response['arr_data']['Street'] + " \r\n"  

            if 'Location' in response['arr_data']:
                message += "*Mahali(GPS):* " + response['arr_data']['Location'] + " \r\n"  


            message += f"\r\n\n*Declaration (Tamko): Ninakiri kwamba maelezo yaliyotolewa hapo juu pamoja na muhtasari wake ni sahihi na ya ukweli. Kama sivyo nitawajibika ipasavyo."
        
        elif response['status'] == 'failed':
            message = response['error_msg'] 

        """response"""
        return JsonResponse({"message": message, "arr_message": []})

        

