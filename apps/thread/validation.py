import re
import requests
import json
import logging
from datetime import datetime, date
from django.http import JsonResponse
from apps.thread.models import *


def validate_numeric(uuid, key, language):
    """Validate numeric value"""
    number_pattern = "^\\d+$"
    if re.match(number_pattern, key):
        return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Namba pekee zinahitajika hapa.'
        elif language == "EN":
            message =  "Only namba required here." 
        #response      
        return {'error': True, 'message': message}


def validate_required(uuid, key):
    pass


def validate_email(uuid, key, language):
    """validate email address"""
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    #remove space
    key = key.replace(' ', '')

    if re.match(pattern, key):
      return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea kuandika barua pepe. mfano: info@lainafinance.co.tz'
        elif language == "EN":
            message =  "Valid email required here. e.g: info@lainafinance.co.tz" 

        #response 
        return {'error': True, 'message': message}


def validate_phone(uuid, key, language):
    """Validate phone number"""
    pattern = "^0[6-7]{1}[0-9]{8}$"

    #remove space
    key = key.replace(' ', '')

    if re.match(pattern, key):
      return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea kuandika namba ya simu. mfano: 0768170000'
        elif language == "EN":
            message =  "Valid phone required here. e.g: 0768170000"

        #response
        return {'error': True, 'message': message}
    

def validate_NIN(uuid, key, language):
    """validate national identification ID"""
    pattern = "^[0-9]{20}$"

    #remove space
    key = key.replace(' ', '')

    if re.match(pattern, key):
      return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea kuandika kitambulisho cha taifa.'
        elif language == "EN":
            message =  "Valid NIDA Number required here."

        #response
        return {'error': True, 'message': message}


def validate_DL(uuid, key, language):
    """validate Driver Licence => 4002759734"""
    pattern = "^400[0-9]{7}$"

    #remove space
    key = key.replace(' ', '')

    if re.match(pattern, key):
      return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea kuandika leseni ya udereva.'
        elif language == "EN":
            message =  "Valid Driver Licence required here."

        #response
        return {'error': True, 'message': message}


def validate_date(uuid, key, language):
    """validate date format"""
    format = "%d-%m-%Y"

    # checking if format matches the date
    res = True
    
    # using try-except to check for truth value
    try:
        res = bool(datetime.strptime(key, format))
    except ValueError:
        res = False

    """check if validation pass on date format"""
    if res == True:
        return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea kuandika tarehe, tafadhali rudia. Mfano: 08-11-2023'
        elif language == "EN":
            message =  "Only valid date required here. E.g: 08-11-2023"

        #response    
        return {'error': True, 'message': message}


def validate_past_date(uuid, key, language):
    """validate less than today than date"""
    format = "%d-%m-%Y"

    # checking if format matches the date
    res = True
    
    # using try-except to check for truth value
    try:
        res = bool(datetime.strptime(key, format))
    except ValueError:
        res = False

    """check if validation pass on date format"""
    if res == True:
        """comparing menu"""
        past = datetime.strptime(key, "%d-%m-%Y")
        present = datetime.now() 
 
        if past.date() <= present.date():
            """validation True"""
            return {'error': False, 'value': key}
        else:
            message = ""
            if language == "SW":
                message = 'Tarehe haitakiwi kuzidi tarehe ya leo'
            elif language == "EN":
                message =  "Date should not exceed Today Date"

            """Invalid input"""
            return {'error': True, 'message': message}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea kuandika tarehe, tafadhali rudia. mfano: 13-04-2023'
        elif language == "EN":
            message =  "only valid date required here. e.g: 13-04-2023"

        """Invalid input"""
        return {'error': True, 'message': message}


def validate_village(uuid, key, language):
    """validate for village"""
    try:
        request = requests.get("", data={"village": key})

        # The following line give us the response code
        if request.status_code == 200:
            response = request.json()

            if response['no_of_village'] == 1:
                #response  
                return {'error': False, 'value': key, 'data': 'NEXT_MENU'}
            elif response['no_of_village'] > 1:
                #response  
                return {'error': False, 'value': key, 'data': 'WARD_MENU'}
            elif response['no_of_village'] == 0:
                message = ""
                if language == "SW":
                    message = 'Umekosea kijiji/mtaa. Tafadhali rudia'
                elif language == "EN":
                    message =  "Wrong village name entered, please enter valid village." 
                #response      
                return {'error': True, 'message': message}
    except requests.exceptions.HTTPError as errh:
        logging.info("Http Error:" + errh)

    except requests.exceptions.ConnectionError as errc:
        logging.info("Error Connecting:" + errc)

    except requests.exceptions.Timeout as errt:
        logging.info("Timeout Error:" + errt)

    except requests.exceptions.RequestException as err:
        logging.info("OOps: Something Else:" + err)
       


def validate_ward(uuid, key, language):
    """validate ward"""
    village_thread = Thread.objects.filter(flag='thread_village').first()

    """GET data from previous thread"""
    thread_session = ThreadSession.objects.filter(thread_id=village_thread.pk, uuid=uuid).first()
    village = thread_session.values
    
    try:
        request = requests.get("", data={"village": village, "ward": key})

        # The following line give us the response code
        if request.status_code == 200:
            response = request.json()

    except requests.exceptions.HTTPError as errh:
        logging.info("Http Error:" + errh)

    except requests.exceptions.ConnectionError as errc:
        logging.info("Error Connecting:" + errc)

    except requests.exceptions.Timeout as errt:
        logging.info("Timeout Error:" + errt)

    except requests.exceptions.RequestException as err:
        logging.info("OOps: Something Else:" + err)






