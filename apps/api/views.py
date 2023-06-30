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
        logging.info(response)

        if response['status'] == 'success':
            #construct message
            message = "*Hakiki Taarifa zako* \n\n" \
            
            if 'text' in response['arr_data']:
                message += "*Maelezo ya Tukio:* " + response['arr_data']['text'] + " \r\n"
                
            if 'village' in response['arr_data']:
                message += "*Kijiji/Mtaa:* " + response['arr_data']['village'] + " \r\n" 

            if 'ward' in response['arr_data']:
                message += "*Kata:* " + response['arr_data']['ward'] + " \r\n" 

            if 'date' in response['arr_data']:
                message += "*Tarehe ya Tukio:* " + response['arr_data']['date'] + " \r\n"  

            if 'street' in response['arr_data']:
                message += "*Jina Maarufu la Eneo:* " + response['arr_data']['street'] + " \r\n"  

            if 'location' in response['arr_data']:
                message += "*Mahali(GPS):* " + response['arr_data']['location'] + " \r\n"  


            message += f"\r\n\n*Hakiki taarifa zako na endelea kwa kuzituma."
        
        elif response['status'] == 'failed':
            message = response['error_msg'] 

        """response"""
        return JsonResponse({"message": message, "arr_message": []})

        

