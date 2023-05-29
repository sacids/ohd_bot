import os
import random
import string
import requests
import json
import logging
from django.http import JsonResponse
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
        thread_response = self.process_thread(thread.id, uuid, language)

        """return response"""
        return thread_response


    def check_thread_link(self, thread_id, key):
        """Check Thread Link"""
        sub_thread = SubThread.objects.filter(thread_id=thread_id)

        if sub_thread.count() > 0:
            sub_thread_key = SubThread.objects.filter(thread_id=thread_id, view_id=key).first()

            if (sub_thread_key):
                thread_link = ThreadLink.objects.filter(
                    thread_id=thread_id, sub_thread_id=sub_thread_key.id)

                if(thread_link):
                    return 'NEXT_MENU'
                else:
                    return 'INVALID_INPUT'
            else:
                return 'INVALID_INPUT'      
        else:
            thread_link = ThreadLink.objects.filter(thread_id=thread_id)

            if(thread_link):
                return 'NEXT_MENU'
            else:
                return 'END_MENU'


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

            """normal response"""
            response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)
        else: 
            response = self.next_thread(phone=phone, uuid=uuid, thread_id=thread_id, key=key, channel=channel, language=language)

        """response"""   
        return response    


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
        sub_thread_key = SubThread.objects.filter(thread_id=thread_id, view_id=key)

        new_response = {}
        if (sub_thread_key):
            sub_thread_key = sub_thread_key.first()

            """thread link"""
            thread_link = ThreadLink.objects.filter(thread_id=thread_id, sub_thread_id=sub_thread_key.id)

            if(thread_link):
                thread_link = thread_link.first()

                """create new session"""
                self.create_thread_session(phone=phone, thread_id=thread_link.link_id, uuid=uuid, channel=channel)

                """process thread"""
                request = self.process_thread(thread_link.link_id, uuid, language)
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
                    "message_type": response['message_type'], 
                    "arr_trees": response['arr_trees'], 
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
                    "message_type": "TEXT", 
                    "arr_trees": [], 
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
                request = self.process_thread(thread_link.link_id, uuid, language)
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
                    "message_type": response['message_type'], 
                    "arr_trees": response['arr_trees'], 
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
                    "message_type": "TEXT", 
                    "arr_trees": [], 
                    "action": action, 
                    "actionURL": actionURL 
                }

        """return response"""
        return JsonResponse(new_response)


    def process_thread(self, thread_id, uuid, language):
        """Process Thread"""
        thread       = Thread.objects.get(pk=thread_id)
        message_type = thread.message_type
        message      = thread.title

        #switch language
        if (thread.db_flag == "thread_services"):
            language = self.switch_language(uuid, thread.db_flag, language) 
        
        #change message based on language
        if language == "SW":
            message = thread.title_sw
        elif language == "EN":
            message = thread.title_en_us  
    
        """if there response"""
        sub_threads = SubThread.objects.filter(thread_id=thread_id).order_by('view_id')

        arr_trees = []
        if(sub_threads):
            for val in sub_threads:
                title = val.title
                description = val.description

                #change title and description based on language
                if language == "SW":
                    title       = val.title_sw
                    description = val.description_sw
                elif language == "EN":
                    title       = val.title_en_us
                    description = val.description_en_us   

                #create tree
                tree = {
                    "view_id" : val.view_id,
                    "title": title,
                    "description": description
                }
                arr_trees.append(tree)

        """thread response"""    
        thread_response = {
            "status": 'success', 
            'language': language,
            "message": message, 
            "message_type": message_type, 
            "arr_trees": arr_trees
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

                if sub_thread.title == "English":
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


    def process_data(self, **kwargs):
        """Process data for processing"""
        uuid  = kwargs["uuid"]

        """thread sessions"""
        thread_sessions = ThreadSession.objects.filter(code=uuid)
        print(thread_sessions)

        if thread_sessions:
            arr_data = {}
            for t_session in thread_sessions:
                thread = Thread.objects.get(pk=t_session.thread_id)
                sub_thread = SubThread.objects.filter(thread_id=thread.id)

                thread_value = ''
                if sub_thread:
                    sub_thread_value = SubThread.objects.filter(thread_id=thread.id, view_id=t_session.values).first()

                    if sub_thread_value:
                        thread_value = sub_thread_value.title
                else:
                    thread_value = t_session.values   

                """assign all data to array"""
                if thread.label is not None and thread_value is not None:
                    arr_data[thread.label] = thread_value   

            """response"""
            return JsonResponse({'status': 'success', 'arr_data': arr_data})
        else:
            return JsonResponse({'status': 'failed', 'error_msg': 'No any data!'})