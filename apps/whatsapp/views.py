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

    wrapper = WhatsAppWrapper()

    print("key => " + message)
    print("from number => " + from_number)

    """process thread"""
    request = process_threads(from_number=from_number, key=message)
    response = json.loads(request.content)

    """return response to telerivet"""
    return HttpResponse(json.dumps({
        'messages': [
            {"content": response}
        ]
    }), 'application/json') 


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
                message_resp = wrapper.get_message(data)

                """process thread"""
                request = process_threads(from_number=from_number, key=message_resp)
                response = json.loads(request.content)

            elif message_type == "interactive":
                message_resp = wrapper.get_interactive_message(data)

                intractive_type = message_resp.get("type")
                message_id = message_resp[intractive_type]["id"]
                message_text = message_resp[intractive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")

                """process thread"""
                request = process_threads(from_number=from_number, key=message_id)
                response = json.loads(request.content)

            elif message_type == 'location':
                message_location = wrapper.get_location(data)

                """latitude and longitude"""
                latitude     = message_location["latitude"]
                longitude    = message_location["longitude"]
                new_location = f"{latitude} {longitude}"
                logging.info(f"{from_number} sent {new_location}")

                """process thread"""
                request = process_threads(from_number=from_number, key=new_location)
                response = json.loads(request.content)

            elif message_type == 'image':
                image = wrapper.get_image(data)  

                """get image data"""
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = wrapper.query_media_url(image_id)
                image_filename = wrapper.download_media(image_url, mime_type, image_id)
                logging.info(f"{from_number} sent file {image_filename}")

                """process thread"""
                request = process_threads(from_number=from_number, key=image_filename)
                response = json.loads(request.content)

            elif message_type == 'document':
                file = wrapper.get_document(data)

                file_id, mime_type = file["id"], file["mime_type"]
                file_url = wrapper.query_media_url(file_id)
                file_filename = wrapper.download_media(file_url, mime_type, file_id)
                logging.info(f"{from_number} sent file {file_filename}")

                """process thread"""
                request = process_threads(from_number=from_number, key=file_filename)
                response = json.loads(request.content)

            elif message_type == 'audio':
                audio = wrapper.get_audio(data)

                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = wrapper.query_media_url(audio_id)
                audio_filename = wrapper.download_media(audio_url, mime_type, audio_id)
                logging.info(f"{from_number} sent audio {audio_filename}")

                """process thread"""
                request = process_threads(from_number=from_number, key=audio_filename)
                response = json.loads(request.content)

            elif message_type == "video":
                video = wrapper.get_video(data)

                video_id, mime_type = video["id"], video["mime_type"]
                video_url = wrapper.query_media_url(video_id)
                video_filename = wrapper.download_media(video_url, mime_type, video_id)
                logging.info(f"{from_number} sent video {video_filename}")  

                """process thread"""
                request = process_threads(from_number=from_number, key=video_filename)
                response = json.loads(request.content)  

            """data"""
            message = response['message']
            show_type = response['message_type']
            arr_trees = response['arr_trees']     

            """structure the whatsapp response""" 
            response = wrapper.structure_response(from_number, show_type, message, arr_trees)
            logging.info(response)

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

    """initiate variables"""
    message = ""
    message_type = ""
    arr_trees = []

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
        request = wrapper.init_thread(phone=from_number, flag="thread_start", channel="WHATSAPP") 
        response = json.loads(request.content)

        """variables"""
        message = response['message']
        message_type = response['message_type']
        arr_trees = response['arr_trees']
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
                request = wrapper.init_thread(phone=from_number, flag="thread_services", channel="WHATSAPP") 
                response = json.loads(request.content)

                """variables"""
                message = response['message']
                message_type = response['message_type']
                arr_trees = response['arr_trees']

            else:
                m_session = ThreadSession.objects.filter(phone=from_number, active=0).latest('id')
                thread_response = wrapper.check_thread_link(m_session.thread_id, key) 

                """ menu session data """
                OD_uuid = m_session.code
                OD_thread_id = m_session.thread_id

                if thread_response == 'NEXT_MENU':
                    """result"""
                    request = wrapper.validate_thread(phone=from_number, uuid=OD_uuid, thread_id=OD_thread_id, key=key, channel="WHATSAPP")
                    response = json.loads(request.content)

                    """status"""
                    status = response['status']

                    if status == 'success':
                        """update thread session"""
                        m_session.active = 1
                        m_session.values = response['value']
                        m_session.save()

                        """variables"""
                        message = response['message']
                        message_type = response['message_type']
                        arr_trees = response['arr_trees']

                        """check for action = None"""
                        if(response['action'] is not None):
                            """process data"""
                            my_data = wrapper.process_data(uuid=OD_uuid)
                            logging.info(my_data)

                    
                    elif status == 'failed':
                        """TODO: if validation failed"""
                        pass

                elif thread_response == 'INVALID_INPUT':
                    """invalid input"""
                    message = "Chaguo batili, tafadhali chagua tena!"
                    message_type = response['message_type']
                    arr_trees = response['arr_trees']

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

                        """TODO: perform any action in here => PUSH, CALL"""

                    """initiate thread session"""
                    message = "Asante kwa kutumia huduma za Laina Finance" 
                    message_type = "TEXT"  
        else:
            if key.upper() == "LAINA" or key.upper() == "HUDUMA":
                """update all menu sessions"""
                ThreadSession.objects.filter(phone=from_number).update(active=1)

                """init service menu"""
                request = wrapper.init_thread(phone=from_number, flag="thread_services", channel="WHATSAPP") 
                response = json.loads(request.content)

                """variables"""
                message = response['message']
                message_type = response['message_type']
                arr_trees = response['arr_trees']
            else:
                message = "Karibu Laina Finance, kutumia huduma hii andika neno LAINA au HUDUMA."
                message_type = "TEXT" 

    """return response"""
    return JsonResponse({"status": "success", "message": message, "message_type": message_type, "arr_trees": arr_trees})

    
def push_data(**kwargs):
    """push data to external API"""
    payload   = kwargs['payload']
    actionURL = kwargs['action_url']

    """push data"""
    response = requests.post(f"{actionURL}", data = json.dumps(payload), headers={"Content-Type": "application/json; charset=utf-8"})
    logging.info(response.json())
        
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})


