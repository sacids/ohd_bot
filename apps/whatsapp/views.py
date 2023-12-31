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
API_URL = "https://graph.facebook.com/v17.0/"


def testing(request):
    """message"""
    message = request.GET.get('message')
    from_number = request.GET.get('from_number')

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
def send_test_message(request):
    """send test message"""
    wrapper = WhatsAppWrapper()

    # thread = Thread.objects.get(pk="8f13d90b-8a50-4b7b-9bbb-e960d78b4c82")

    message = "Hello Tanzania\nkaribu kwetu"

    #send text message now
    # response = wrapper.send_text_message("255717705746", thread.title.replace("<br>", "\n")) 
    # logging.info(response)

    return HttpResponse(message.replace("<br>", "\n"), status=200)



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

                #image path
                image_path = f"https://net.sacids.org/{image_filename}"

                """process thread"""
                request = process_threads(from_number=from_number, key=image_path)
                response = json.loads(request.content)

            elif message_type == 'document':
                file = wrapper.get_document(data)

                file_id, mime_type = file["id"], file["mime_type"]
                file_url = wrapper.query_media_url(file_id)
                file_filename = wrapper.download_media(file_url, mime_type, file_id)
                logging.info(f"{from_number} sent file {file_filename}")

                #file path
                file_path = f"https://net.sacids.org/{file_filename}"

                """process thread"""
                request = process_threads(from_number=from_number, key=file_path)
                response = json.loads(request.content)

            elif message_type == 'audio':
                audio = wrapper.get_audio(data)

                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = wrapper.query_media_url(audio_id)
                audio_filename = wrapper.download_media(audio_url, mime_type, audio_id)
                logging.info(f"{from_number} sent audio {audio_filename}")

                #audio path
                audio_path = f"https://net.sacids.org/{audio_filename}"

                """process thread"""
                request = process_threads(from_number=from_number, key=audio_path)
                response = json.loads(request.content)

            elif message_type == "video":
                video = wrapper.get_video(data)

                video_id, mime_type = video["id"], video["mime_type"]
                video_url = wrapper.query_media_url(video_id)
                video_filename = wrapper.download_media(video_url, mime_type, video_id)
                logging.info(f"{from_number} sent video {video_filename}")  

                #video path
                video_path = f"https://net.sacids.org/{video_filename}"

                """process thread"""
                request = process_threads(from_number=from_number, key=video_path)
                response = json.loads(request.content)  

            """data"""
            language     = response['language']
            message      = response['message']
            attachment   = response['attachment']
            show_type    = response['message_type']
            arr_trees    = response['arr_trees']  
            main_thread  = response['main_thread']   

            """structure the whatsapp response""" 
            response = wrapper.structure_response(from_number, show_type, language, message, attachment, arr_trees, main_thread)
            logging.info("===== Facebook Response ====")
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
    language = "SW"
    message = ""
    attachment = None
    message_type = ""
    arr_trees = []
    main_thread = False

    """thread wrapper"""
    wrapper = ThreadWrapper()

    """profile"""
    customer = Customer.objects.filter(phone=from_number)

    #deal with language
    lbLanguage = CustomerLanguage.objects.filter(phone=from_number)

    if lbLanguage.count() > 0:
        lbLanguage = lbLanguage.first()
        #update default language
        language = lbLanguage.language
    else:
        #insert new language
        lbLanguage = CustomerLanguage()
        lbLanguage.phone = from_number
        lbLanguage.language = "EN"  
        lbLanguage.save()     

    if customer.count() == 0:
        #TODO: Query user details to the main system



        """create profile"""
        customer = Customer()
        customer.phone = from_number
        customer.save()

        """init thread"""
        request = wrapper.init_thread(phone=from_number, flag="thread_services", channel="WHATSAPP", language=language) 
        response = json.loads(request.content)

        """variables"""
        message = response['message']
        attachment = response['attachment']
        message_type = response['message_type']
        arr_trees = response['arr_trees']
    else:
        """initialize citizen"""
        customer = customer.first()

        """Follow thread session and Trigger follow up menu"""
        thread_session = ThreadSession.objects.filter(phone=from_number, active=0)

        if thread_session.count() > 0:
            if key.upper() == "TAARIFA" or key.upper() == "TUKIO" or key.upper() == "HI" or key.upper() == "HELLO" or key.upper() == "MAMBO" or key.upper() == "ANZA" or key.upper() == "HABARI" or key == "0" or key == "#" or key == "":
                """update all menu sessions"""
                ThreadSession.objects.filter(phone=from_number).update(active=1)

                """init service menu"""
                request = wrapper.init_thread(phone=from_number, flag="thread_services", channel="WHATSAPP", language=language) 
                response = json.loads(request.content)

                """variables"""
                language     = response['language']
                message      = response['message']
                attachment   = response['attachment']
                message_type = response['message_type']
                arr_trees    = response['arr_trees']
                main_thread  = response['main_thread']
            else:
                m_session = ThreadSession.objects.filter(phone=from_number, active=0).latest('id')
                thread_response = wrapper.check_thread_link(m_session.thread_id, key) 

                """ menu session data """
                OD_uuid = m_session.code
                OD_thread_id = m_session.thread_id

                if thread_response['link'] == 'API_MENU':
                    """Call API """
                    payload = {
                        'msg': key,
                        'msisdn': from_number,
                        'sessionId': OD_uuid
                    }
                    request = requests.post(thread_response['api'], params=payload)
                    response = request.json()
                    
                    """variables"""
                    language     = language
                    message      = response['message']
                    message_type = "TEXT"
                    arr_trees    = []
                    main_thread  = response['main_thread']

                elif thread_response['link'] == 'NEXT_MENU':
                    """update thread session"""
                    m_session.active = 1
                    m_session.values = key
                    m_session.save()
                    
                    """result"""
                    request = wrapper.validate_thread(phone=from_number, uuid=OD_uuid, thread_id=OD_thread_id, key=key, channel="WHATSAPP", language=language)
                    response = json.loads(request.content)

                    """status"""
                    status = response['status']

                    if status == 'success':
                        """update thread session"""
                        m_session.values = response['value']
                        m_session.save()

                        """variables"""
                        language     = response['language']
                        message      = response['message']
                        attachment   = response['attachment']
                        message_type = response['message_type']
                        arr_trees    = response['arr_trees']
                        main_thread  = response['main_thread']

                        """check for action = None"""
                        if(response['action'] is not None):
                            """process data"""
                            my_data = wrapper.process_data(uuid=OD_uuid)
                            my_data = json.loads(my_data.content)

                            if response['action'] == 'REGISTRATION':
                                """create profile"""
                                result = create_profile(phone=from_number, response=my_data)

                    elif status == 'failed':
                        """IF VALIDATION FAIL => update thread session"""
                        m_session.active = 0
                        m_session.save()

                        """variables"""
                        language     = response['language']
                        message      = response['message']
                        attachment   = response['attachment']
                        message_type = response['message_type']
                        arr_trees    = response['arr_trees']
                        main_thread  = False

                elif thread_response['link'] == 'INVALID_INPUT':
                    """invalid input"""
                    if language == "SW":
                        message = "Chaguo batili, tafadhali chagua tena."
                    elif language == "EN":
                        message = "Invalid input, Please select option again."
                    message_type = "TEXT"

                elif thread_response['link'] == 'END_MENU':
                    """update and end thread session"""
                    ThreadSession.objects.filter(code=OD_uuid).update(active=1)

                    """query menu data"""
                    thread = Thread.objects.filter(pk=OD_thread_id)

                    if thread.count() > 0:
                        thread = thread.first()

                        """process data"""
                        my_data = wrapper.process_data(uuid=OD_uuid)
                        logging.info(my_data)

                        """TODO: perform any action in here => REGISTRATION, PUSH, CALL"""

                    """initiate thread session"""
                    if language == "SW":
                        message = "Asante kwa kuripoti taarifa, tunazichambua taarifa zako na kuzifanyia kazi." 
                    elif language == "EN":
                        message = "Thank you for reporting, we will review reporting information and respond to it."
                    message_type = "TEXT"  
        else:
            if key.upper() == "TAARIFA" or key.upper() == "TUKIO" or key.upper() == "HI" or key.upper() == "HELLO" or key.upper() == "MAMBO" or key.upper() == "ANZA" or key.upper() == "HABARI" or key == "0" or key == "#" or key == "":
                """update all menu sessions"""
                ThreadSession.objects.filter(phone=from_number).update(active=1)

                """init service menu"""
                request = wrapper.init_thread(phone=from_number, flag="thread_services", channel="WHATSAPP", language=language) 
                response = json.loads(request.content)

                """variables"""
                language     = response['language']
                message      = response['message']
                attachment   = response['attachment']
                message_type = response['message_type']
                arr_trees    = response['arr_trees']
                main_thread  = response['main_thread']
            else:
                if language == "SW":
                    message = "Karibu kituo cha Taifa cha Operesheni na Mawasiliano ya Dharura, andika/tuma neno TAARIFA, TUKIO."
                elif language == "EN": 
                    message = "Welcome National Disaster Center, write TAARIFA or TUKIO for reporting new event."   
                message_type = "TEXT" 

    """return response"""
    return JsonResponse({"status": "success", "language": language, "message": message, "attachment": attachment, "message_type": message_type, "arr_trees": arr_trees, "main_thread": main_thread})

    
def push_data(**kwargs):
    """push data to external API"""
    payload   = kwargs['payload']
    actionURL = kwargs['action_url']

    """push data"""
    response = requests.post(f"{actionURL}", data = json.dumps(payload), headers={"Content-Type": "application/json; charset=utf-8"})
    logging.info(response.json())
        
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})


def create_profile(**kwargs):
    """create profile for CUSTOMER"""
    phone    = kwargs['phone']
    response = kwargs['response']

    """query for customer"""
    customer = Customer.objects.filter(phone=phone).first()

    if customer:
        """process data"""
        if 'Phone' in response['arr_data']:
            customer.phone2  = response['arr_data']['Phone']

        if 'NIN' in response['arr_data']:    
            customer.id_number  = response['arr_data']['NIN']

        customer.status = 'COMPLETED'
        customer.save()

    return JsonResponse({"error": False, 'success_msg': "Customer data updated"})    


