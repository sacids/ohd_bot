import json
import logging
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .classes import WhatsAppWrapper
from apps.thread.classes import ThreadWrapper
from apps.thread.models import *
from decouple import config
import logging

VERIFY_TOKEN = config('WHATSAPP_VERIFY_TOKEN')
API_URL = "https://graph.facebook.com/v16.0/"


def testing(request):
    """message"""
    message = request.GET.get('message')
    from_number = request.GET.get('from_number')

    print("key => " + message)
    print("from number => " + from_number)

    """process thread"""
    new_message = process_threads(from_number=from_number, key=message)

    """return response to telerivet"""
    return HttpResponse(json.dumps({
        'messages': [
            {"content": new_message}
        ]
    }), 'application/json') 

@csrf_exempt
def send_interactive_sms(request):
    """__summary__: Get message from the webhook"""
    wrapper = WhatsAppWrapper()

    from_number = "255717705746"
    new_message = "Welcome to our service"

    """send message"""
    response = wrapper.send_interactive_message(from_number, new_message)

    logging.info("Response => ")
    logging.info(response)


@csrf_exempt
def facebook(request):
    """__summary__: Get message from the webhook"""
    wrapper = WhatsAppWrapper()

    if request.method == "GET":
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status = 200)
        else:
            return HttpResponse('Authentication failed. Invalid Token.', status=403)    

    if request.method == 'POST':
        data = json.loads(request.body)
        logging.info(data)

        """extract => field, from, key, message_type"""
        field = data["entry"][0]["changes"][0]["field"]

        """check if field not messages and reply 400 response"""
        if field != 'messages':
            return HttpResponse('Invalid data', 400)

        """new message"""
        new_message = wrapper.get_mobile(data)

        if new_message:
            from_number = wrapper.get_mobile(data)
            profile_name = wrapper.get_profile_name(data)
            message_type = wrapper.get_message_type(data)
            timestamp = wrapper.get_message_timestamp(data)
            facebook_id = wrapper.get_messageId(data)

            if message_type == 'text':
                message = wrapper.get_message(data)

                """process thread"""
                new_message = process_threads(from_number=from_number, key=message)

                """send message"""
                response = wrapper.send_text_message(from_number, new_message)
                logging.info("Response From Facebook => ")
                logging.info(response)

            elif message_type == "interactive":
                message = wrapper.get_message(data)

                """process thread"""
                new_message = process_threads(from_number=from_number, key=message)

                """send message"""
                response = wrapper.send_interactive_message(from_number, new_message)

            elif message_type == 'location':
                message_location = wrapper.get_location(data)

                """latitude and longitude"""
                latitude     = message_location["latitude"]
                longitude    = message_location["longitude"]
                new_location = f"{latitude} {longitude}"

                """process thread"""
                new_message = process_threads(from_number=from_number, key=new_location)

                """send message"""
                response = wrapper.send_text_message(from_number, new_message)

            elif message_type == 'image':
                image = wrapper.get_image(data)  

                """get image data"""
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = wrapper.query_media_url(image_id)
                logging.info(image_url)

                """TODO: save image to a folder"""

                """process thread"""
                new_message = process_threads(from_number=from_number, key="image_url")

                """send message"""
                response = wrapper.send_text_message(from_number, new_message)
            elif message_type == 'document':
                """process thread"""
                new_message = process_threads(from_number=from_number, key="document_url")

                """send message"""
                response = wrapper.send_text_message(from_number, new_message)
        else:
            delivery = wrapper.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")

        """return response"""
        return HttpResponse('success', status=200)    


def process_threads(**kwargs):
    """process all the threads"""
    from_number = kwargs['from_number']
    key         = kwargs['key']

    """initiate message"""
    message = ""

    """thread wrapper"""
    wrapper = ThreadWrapper()

    """profile"""
    customer = Customer.objects.filter(phone=from_number)

    if customer.count() == 0:
        """create profile"""
        customer = Customer()
        customer.phone = from_number
        customer.save()

        """init thread"""
        message = wrapper.init_thread(phone=from_number, flag="thread_start", channel="WHATSAPP") 
    else:
        """initialize citizen"""
        customer = customer.first()

        """Follow thread session and Trigger follow up menu"""
        thread_session = ThreadSession.objects.filter(phone=from_number, active=0) 

        if thread_session.count() > 0:
            if key.upper() == "LAINA" or key.upper() == "HUDUMA":
                """update all menu sessions"""
                ThreadSession.objects.filter(phone=from_number).update(active=1)

                """init service menu"""
                message = wrapper.init_thread(phone=from_number, flag="thread_services", channel="WHATSAPP") 
            else:
                m_session = ThreadSession.objects.filter(phone=from_number, active=0).latest('id')
                thread_response = wrapper.check_thread_link(m_session.thread_id, key) 

                """ menu session data """
                OD_uuid = m_session.code
                OD_thread_id = m_session.thread_id

                if thread_response == 'NEXT_MENU':
                    """result"""
                    result = wrapper.validate_thread(phone=from_number, uuid=OD_uuid, thread_id=OD_thread_id, key=key, channel="WHATSAPP")
                    data = json.loads(result.content)

                    """status"""
                    status = data['status']

                    if status == 'success':
                        """update thread session"""
                        m_session.active = 1
                        m_session.values = data['value']
                        m_session.save()

                        """message"""
                        message = data['message']

                        """check for action = None"""
                        if(data['action'] is not None):
                            """process data"""
                            my_data = wrapper.process_data(uuid=OD_uuid)
                            logging.info(my_data)

                            if data['action'] == 'PUSH':
                                """update and end thread session"""
                                ThreadSession.objects.filter(uuid=OD_uuid).update(active=1)

                                """push data"""
                                result = push_data(payload=my_data, action_url=data['action_url'])
                    
                    elif status == 'failed':
                        """message"""
                        message = data['message']

                elif thread_response == 'INVALID_INPUT':
                    """invalid input"""
                    message = "Chaguo batili, tafadhali chagua tena!"
                elif thread_response == 'END_MENU':
                    """update and end thread session"""
                    ThreadSession.objects.filter(code=OD_uuid).update(active=1)

                    """query menu data"""
                    thread = Thread.objects.filter(pk=OD_thread_id)

                    if thread.count() > 0:
                        thread = thread.first()

                        """process data"""
                        my_data = wrapper.process_data(uuid=OD_uuid)
                        logging.info(my_data)

                        if thread.action == 'PUSH':
                            """push data"""
                            result = push_data(payload=my_data, action_url=thread.action_url)

                    """initiate thread session"""
                    message = "End of session"   
        else:
            if key.upper() == "LAINA" or key.upper() == "HUDUMA":
                """update all menu sessions"""
                ThreadSession.objects.filter(phone=from_number).update(active=1)

                """init service menu"""
                message = wrapper.init_thread(phone=from_number, flag="thread_services", channel="WHATSAPP") 
            else:
                message = "Karibu Laina Finance, kutumia huduma hii andika neno LAINA au HUDUMA."

    """return message"""
    return message

    
def push_data(**kwargs):
    """push data to external API"""
    payload   = kwargs['payload']
    actionURL = kwargs['action_url']

    """push data"""
    response = requests.post(f"{actionURL}", data = json.dumps(payload), headers={"Content-Type": "application/json; charset=utf-8"})
    logging.info(response.json())
        
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})


