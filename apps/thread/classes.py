import os
import random
import string
import requests
import json
import logging
from django.http import JsonResponse
from .validation import *
from .models import *

class ThreadWrapper:
    """class control all the thread in the chatbot"""
    BASE_URL   = "http://127.0.0.1:8000/"

    def __init__(self):
        pass


    def init_thread(self, **kwargs):
        """ Initialize first thread """
        phone          = kwargs['phone']
        flag           = kwargs['flag']
        channel        = kwargs['channel']
        language       = kwargs['language']

        """first thread"""
        thread = Thread.objects.get(db_flag=flag)

        """random code"""
        uuid = ''.join(random.choices(string.ascii_uppercase, k=12))

        """Create menu session"""
        session_id = self.create_thread_session(phone=phone, thread_id=thread.id, uuid=uuid, channel=channel)

        """response"""
        thread_response = self.process_thread(phone, thread.id, uuid, language)

        """return response"""
        return thread_response


    def check_thread_link(self, thread_id, key):
        """Check Thread Link"""
        sub_thread = SubThread.objects.filter(thread_id=thread_id)

        if sub_thread.count() > 0:
            # Number Pattern
            pattern = "^\\d+$"

            if re.match(pattern, key):
                sub_thread_key = SubThread.objects.filter(thread_id=thread_id, view_id=key)

                if sub_thread_key.count() > 0:
                    sub_thread_key = sub_thread_key.first()

                    #thread link
                    thread_link = ThreadLink.objects.filter(thread_id=thread_id, sub_thread_id=sub_thread_key.id)

                    if thread_link.count() > 0:
                        thread_link = thread_link.first()

                        if thread_link.linking_type == "RESPONSE_THREAD":
                            return {"link": "NEXT_MENU", "api": None}
                        elif thread_link.linking_type == "RESPONSE_API":
                            return {"link": "API_MENU", "api": thread_link.api_url}
                    else:
                        return {"link": "INVALID_INPUT", "api": None}
                else:
                    return {"link": "INVALID_INPUT", "api": None} 
            else:
                return {"link": "INVALID_INPUT", "api": None}       
        else:
            thread_link = ThreadLink.objects.filter(thread_id=thread_id)

            if thread_link.count() > 0:
                return {"link": "NEXT_MENU", "api": None}
            else:
                return {"link": "END_MENU", "api": None}


    def validate_thread(self, **kwargs):
        """validation rules"""
        phone       = kwargs['phone']
        uuid        = kwargs['uuid']
        thread_id   = kwargs['thread_id']
        key         = kwargs['key']
        channel     = kwargs['channel']
        language    = kwargs['language']

        """thread"""
        thread = Thread.objects.filter(id=thread_id).first()

        #responses
        response = {}

        if thread.validation is not None:
            """TODO: validate entries"""
            if thread.validation == "NUMERIC":
                validation = validate_numeric(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})
            
            elif thread.validation == "EMAIL":
                validation = validate_email(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "message_type": "TEXT", "arr_trees": []})
            
            elif thread.validation == "PHONE":
                validation = validate_phone(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})
            
            elif thread.validation == "NIN":
                validation = validate_NIN(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})
            
            elif thread.validation == "DL":
                validation = validate_DL(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})   

            elif thread.validation == "DATE":
                validation = validate_date(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})

            elif thread.validation == "PAST_DATE":
                validation = validate_past_date(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})
            
            elif thread.validation == "TIME":
                validation = validate_date(uuid, key, language)

                if validation['error'] == False:
                    response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})
            
            elif thread.validation == "VILLAGE":
                validation = validate_village(uuid, key, language)

                if validation['error'] == False:
                    if validation['data'] == "NEXT_MENU":
                        response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
                    elif validation['data'] == 'WARD_MENU':
                        """current thread"""
                        ct_thread = Thread.objects.filter(flag='thread_ward').first()
                        response = self.current_thread(phone=phone, uuid=uuid, thread_id=ct_thread.pk, key=key, channel=channel, language=language)   
                elif validation['error'] == True:
                   response = JsonResponse({"status": 'failed', 'language': language, "message": validation['message'], "attachment": None, "message_type": "TEXT", "arr_trees": []})
        else: 
            response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)

        """response"""   
        return response    


    def current_thread(self, **kwargs):
        """Triggering current thread"""
        phone       = kwargs['phone']
        uuid        = kwargs['uuid']
        thread_id   = kwargs['thread_id']
        key         = kwargs['key']
        channel     = kwargs['channel']
        language    = kwargs['language']

        """action"""
        action = None
        actionURL = None

        """thread"""
        thread = Thread.objects.get(pk=thread_id)

        """create new session"""
        session_id = self.create_thread_session(phone=phone, thread_id=thread.pk, uuid=uuid, channel=channel)

        """process thread"""
        request = self.process_thread(phone, thread.pk, uuid, language)
        response = json.loads(request.content)

        """new response"""
        new_response = {
            'status': 'success', 
            'value': key, 
            'language': response['language'],
            'message': response['message'], 
            'attachment': response['attachment'],
            "message_type": response['message_type'], 
            "arr_trees": response['arr_trees'], 
            "main_thread": response['main_thread'],
            'action': action, 
            'actionURL': actionURL
        }

        """return response"""
        return JsonResponse(new_response)


    def next_thread(self, **kwargs):
        """Triggering Next Thread"""
        phone       = kwargs['phone']
        uuid        = kwargs['uuid']
        thread_id   = kwargs['thread_id']
        key         = kwargs['key']
        channel     = kwargs['channel']
        language    = kwargs['language']

        """thread"""
        thread = Thread.objects.filter(id=thread_id).first()

        """action"""
        action = None
        actionURL = None
   
        """sub thread"""
        sub_thread = SubThread.objects.filter(thread_id=thread_id)

        if sub_thread.count() > 0:
            #response
            new_response = {}
        
            #sub thread key    
            sub_thread_key = SubThread.objects.filter(thread_id=thread_id, view_id=key)

            if sub_thread_key.count() > 0:
                sub_thread_key = sub_thread_key.first()

                """TODO: check for registered or not registered link"""

                """thread link"""
                thread_link = ThreadLink.objects.filter(thread_id=thread_id, sub_thread_id=sub_thread_key.id)

                if(thread_link):
                    thread_link = thread_link.first()

                    """create new session"""
                    self.create_thread_session(phone=phone, thread_id=thread_link.link_id, uuid=uuid, channel=channel)

                    """process thread"""
                    request = self.process_thread(phone, thread_link.link_id, uuid, language)
                    response = json.loads(request.content)

                    """thread action"""
                    thread = Thread.objects.get(pk=thread_link.link_id)

                    if thread.action is not None:
                        action = thread.action
                        actionURL = thread.action_url 

                    """new response"""
                    new_response = {
                        'status': 'success', 
                        'value': key, 
                        'language': response['language'],
                        'message': response['message'], 
                        'attachment': response['attachment'],
                        "message_type": response['message_type'], 
                        "arr_trees": response['arr_trees'], 
                        "main_thread": response['main_thread'],
                        'action': action, 
                        'actionURL': actionURL
                    }
                else:
                    #change title and description based on language
                    if language == "SW":
                        message = "Chaguo batili"
                    elif language == "EN":
                        message = "Invalid Input"

                    """new response"""
                    new_response = {
                        "status": 'success', 
                        'language': language,
                        "message": message, 
                        'attachment': None,
                        "message_type": "TEXT", 
                        "arr_trees": [], 
                        "main_thread": False,
                        "action": action, 
                        "actionURL": actionURL 
                    }    
        else:
            thread_link = ThreadLink.objects.filter(thread_id=thread_id)

            if(thread_link):
                thread_link = thread_link.first()

                """create session"""
                self.create_thread_session(phone=phone, thread_id=thread_link.link_id, uuid=uuid, channel=channel)

                """process thread"""
                request = self.process_thread(phone, thread_link.link_id, uuid, language)
                response = json.loads(request.content)

                """thread action"""
                thread = Thread.objects.get(pk=thread_link.link_id)

                if thread.action is not None:
                    action = thread.action
                    actionURL = thread.action_url 

                """new response"""
                new_response = {
                    'status': 'success', 
                    'value': key, 
                    'language': response['language'],
                    'message': response['message'],
                    'attachment': response['attachment'],
                    "message_type": response['message_type'], 
                    "arr_trees": response['arr_trees'], 
                    "main_thread": response['main_thread'],
                    'action': action, 
                    'actionURL': actionURL
                }
            else:
                #change title and description based on language
                if language == "SW":
                    message = "Chaguo batili"
                elif language == "EN":
                    message = "Invalid Input"

                """new response"""
                new_response = {
                    "status": 'success', 
                    'language': language,
                    "message": message, 
                    'attachment': None,
                    "message_type": "TEXT", 
                    "arr_trees": [], 
                    "main_thread": False,
                    "action": action, 
                    "actionURL": actionURL 
                }

        """return response"""
        return JsonResponse(new_response)


    def process_thread(self, phone, thread_id, uuid, language):
        """Process Thread"""
        thread       = Thread.objects.get(pk=thread_id)
        message_type = thread.message_type
        message      = thread.title
        attachment   = None
             

        #switch language
        if (thread.db_flag == "thread_services"):
            print("language => " + language) 
            language = self.switch_language(uuid, thread.db_flag, language) 
        
        #change message based on language
        if language == "SW":
            message = thread.title_sw
        elif language == "EN":
            message = thread.title_en_us  

        #start processing thread on 
        if thread.action is not None and thread.action == "VERIFICATION":
            #build params
            arr_params = self.build_payload(payload=thread.payload, msisdn=phone, uuid=uuid)

            try:
                request = requests.post(thread.action_url, data=arr_params)

                # The following line give us the response code
                if request.status_code == 200:
                    response = request.json()

                    if response['message'] is not None:
                        message = response['message']

                    if 'attachment' in response:
                        if response['attachment'] is not None:
                            attachment = response['attachment']   

                    arr_trees = []
                    if len(response['arr_message']) > 0:
                        message_type = "TEXT"
                        for val in response['arr_message']:
                            #create tree
                            tree = {
                                "view_id" : val["id"],
                                "title": val["message"]
                            }
                            arr_trees.append(tree) 
                    else:
                        """if there response"""
                        sub_threads = SubThread.objects.filter(thread_id=thread_id).order_by('view_id')

                        if(sub_threads):
                            for val in sub_threads:
                                title = val.title

                                #change title and description based on language
                                if language == "SW":
                                    title       = val.title_sw
                                elif language == "EN":
                                    title       = val.title_en_us 

                                #create tree
                                tree = {
                                    "view_id" : val.view_id,
                                    "title": title
                                }
                                arr_trees.append(tree) 
                else:
                    logging.info("Error Code")
                    logging.info(request.status_code)
                    message = "Taarifa haipo, tafadhali jaribu tena."
                    arr_trees = []

            except requests.exceptions.HTTPError as errh:
                logging.info("Http Error:" + errh)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []
            except requests.exceptions.ConnectionError as errc:
                logging.info("Error Connecting:" + errc)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []

            except requests.exceptions.Timeout as errt:
                logging.info("Timeout Error:" + errt)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []
            except requests.exceptions.RequestException as err:
                logging.info("OOps: Something Else:" + err)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []    
        elif thread.action is not None and thread.action == "PULL":
            #build params
            arr_params = self.build_payload(payload=thread.payload, msisdn=phone, uuid=uuid)

            try:
                request = requests.post(thread.action_url, data=arr_params)

                # The following line give us the response code
                if request.status_code == 200:
                    response = request.json()

                    if response['message'] is not None:
                        message = response['message']

                    if 'attachment' in response:
                        if response['attachment'] is not None:
                            attachment = response['attachment']

                    arr_trees = []
                    if len(response['arr_message']) > 0:
                        message_type = "TEXT"
                        for val in response['arr_message']:
                            #create tree
                            tree = {
                                "view_id" : val["id"],
                                "title": val["message"]
                            }
                            arr_trees.append(tree) 
                    else:
                        """if there response"""
                        sub_threads = SubThread.objects.filter(thread_id=thread_id).order_by('view_id')

                        if(sub_threads):
                            for val in sub_threads:
                                title = val.title

                                #change title and description based on language
                                if language == "SW":
                                    title       = val.title_sw
                                elif language == "EN":
                                    title       = val.title_en_us 

                                #create tree
                                tree = {
                                    "view_id" : val.view_id,
                                    "title": title
                                }
                                arr_trees.append(tree)
                else:
                    logging.info("Error Code")
                    logging.info(request.status_code)
                    message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                    arr_trees = []
            except requests.exceptions.HTTPError as errh:
                logging.info("Http Error:" + errh)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []
            except requests.exceptions.ConnectionError as errc:
                logging.info("Error Connecting:" + errc)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []

            except requests.exceptions.Timeout as errt:
                logging.info("Timeout Error:" + errt)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []
            except requests.exceptions.RequestException as err:
                logging.info("OOps: Something Else:" + err)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []     
        elif thread.action is not None and thread.action == "PUSH":
            #build params
            arr_params = self.build_payload(payload=thread.payload, msisdn=phone, uuid=uuid)
        
            #create payload for sending
            arr_params = {
                'contents': arr_params, 
                'channel': "WHATSAPP", 
                'contact': phone
            }

            try:
                request = requests.post(thread.action_url, data = json.dumps(arr_params), headers={"Content-Type": "application/json; charset=utf-8"})
                logging.info(request)

                # The following line give us the response code
                if request.status_code == 200:
                    response = request.json()
                    
                    if 'message' in response:
                        if response['message'] is not None:
                            message = response['message']

                    if 'attachment' in response:
                        if response['attachment'] is not None:
                            attachment = response['attachment']

                    arr_trees = []
                else:
                    logging.info("Error Code")
                    logging.info(request.status_code)
                    message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                    arr_trees = []

            except requests.exceptions.HTTPError as errh:
                logging.info("Http Error:" + errh)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []
            except requests.exceptions.ConnectionError as errc:
                logging.info("Error Connecting:" + errc)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []

            except requests.exceptions.Timeout as errt:
                logging.info("Timeout Error:" + errt)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []
            except requests.exceptions.RequestException as err:
                logging.info("OOps: Something Else:" + err)
                message = "Huduma haipatikani kwa sasa, Tafadhali jaribu tena baadae."
                arr_trees = []
        else: 
            """if there response"""
            sub_threads = SubThread.objects.filter(thread_id=thread_id).order_by('view_id')

            arr_trees = []
            if(sub_threads):
                for val in sub_threads:
                    title = val.title

                    #change title and description based on language
                    if language == "SW":
                        title       = val.title_sw
                    elif language == "EN":
                        title       = val.title_en_us

                    #create tree
                    tree = {
                        "view_id" : val.view_id,
                        "title": title
                    }
                    arr_trees.append(tree)
        
        #replace message text

        """thread response"""    
        thread_response = {
            "status": 'success', 
            'language': language,
            "message": message, 
            "attachment": attachment,
            "message_type": message_type, 
            "arr_trees": arr_trees,
            "main_thread": thread.main_thread
        } 

        """Return message""" 
        return JsonResponse(thread_response)

    
    def create_thread_session(self, **kwargs):
        """create menu session""" 
        phone   = kwargs['phone']
        thread_id = kwargs['thread_id']
        uuid    = kwargs['uuid']
        channel = kwargs['channel']

        """query thread"""
        thread  = Thread.objects.get(pk=thread_id)

        """create  new session"""
        session = ThreadSession()
        session.phone = phone  
        session.code = uuid
        session.thread_id = thread_id
        session.channel = channel
        session.flag = thread.db_flag
        session.save()

        """return session ID"""
        return session.id


    def switch_language(self, uuid, db_flag, language):
        """switch language"""
        thread_session = ThreadSession.objects.filter(code=uuid,flag=db_flag, active=1)

        if thread_session.count() > 0:
            thread_session = thread_session.first()

            #language values
            lang_val = thread_session.values

            #query for sub thread
            sub_thread = SubThread.objects.filter(thread_id=thread_session.thread.id, view_id=lang_val)

            if sub_thread.count() > 0:
                sub_thread = sub_thread.first()

                if sub_thread.switch_language == 1:
                    from_number = thread_session.phone

                    #query for language
                    lbLanguage = CustomerLanguage.objects.filter(phone=from_number)

                    if lbLanguage.count() > 0:
                        lbLanguage = lbLanguage.first()
                        current_language = lbLanguage.language

                        if current_language == "EN":
                            lbLanguage.language = "SW"
                            language = "SW"
                        elif current_language == "SW":
                            lbLanguage.language = "EN"
                            language = "EN"
                        lbLanguage.save()     
        #return language
        return language


    def build_payload(self, **kwargs):
        """Build Payload""" 
        payload  = kwargs["payload"]  
        msisdn  = kwargs["msisdn"]  
        uuid  = kwargs["uuid"]  

        #process data
        my_data = self.process_data(uuid = uuid)
        my_data = json.loads(my_data.content)

        arr_params = {}
        arr_params['msisdn'] = msisdn
        arr_params['uuid'] = uuid

        if payload is not None:
            arr_payload = payload.split(',')

            for val in arr_payload:
                if val in my_data['arr_data']:
                    arr_params[val] = my_data['arr_data'][val]               
       
        #return params
        return arr_params


    def process_data(self, **kwargs):
        """Process data for processing"""
        uuid  = kwargs["uuid"]

        """thread sessions"""
        thread_sessions = ThreadSession.objects.filter(code=uuid)

        if thread_sessions:
            arr_data = {}
            for t_session in thread_sessions:
                thread = Thread.objects.get(pk=t_session.thread_id)

                #check for data mapping
                if thread.map_data == 1:
                    sub_thread = SubThread.objects.filter(thread_id=thread.id)

                    thread_value = ''
                    if sub_thread:
                        sub_thread_value = SubThread.objects.filter(thread_id=thread.id, view_id=t_session.values).first()

                        if sub_thread_value:
                            thread_value = sub_thread_value.title
                    else:
                        thread_value = t_session.values 

                elif thread.map_data == 0:
                    thread_value = t_session.values           

                """assign all data to array"""
                if thread.label is not None and thread_value is not None:
                    arr_data[thread.label] = thread_value   

            """response"""
            return JsonResponse({'status': 'success', 'arr_data': arr_data})
        else:
            return JsonResponse({'status': 'failed', 'error_msg': 'No any data!'})