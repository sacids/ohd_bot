import re
from datetime import datetime, date
from django.http import JsonResponse
from apps.thread.models import *


def validate_numeric(key, language):
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


def validate_required(key):
    pass


def validate_email(key, language):
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


def validate_phone(key, language):
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
    

def validate_NIN(key, language):
    """validate national identification ID"""
    pattern = "^[0-9]{24}$"

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


def validate_DL(key, language):
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
    

def validate_DL_NIN(key, language):
    """Validate Driver Licence or NIN"""
    NIN_pattern = "^[0-9]{24}$"
    DL_pattern = "^400[0-9]{7}$"

    #remove space
    key = key.replace(' ', '')

    if re.match(DL_pattern, key) or re.match(NIN_pattern, key):
        return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea leseni ya udereva au Kitambulisho cha taifa.'
        elif language == "EN":
            message =  "Valid Driver Licence or NIDA Number required here."

        #response
        return {'error': True, 'message': message}
    

def validate_VN(key, language):
    """validate Vehicle/Motor Cycle Registration Number"""
    VN_pattern = "^T[0-9]{3}[a-zA-Z]{3}$"
    MT_pattern = "^MC[0-9]{3}[a-zA-Z]{3}$"

    #remove space
    key = key.replace(' ', '')

    #force key to be uppercase
    key = key.upper()

    if re.match(VN_pattern, key) or re.match(MT_pattern, key):
        return {'error': False, 'value': key}
    else:
        message = ""
        if language == "SW":
            message = 'Umekosea kuandika namba ya chombo chako. mfano: MC874AXC'
        elif language == "EN":
            message =  "Valid Vehicle/Motorcycle number required here. e.g: MC874AXC"

        #response
        return {'error': True, 'message': message}


def validate_date(key, language):
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
            message = 'Umekosea kuandika tarehe, tafadhali rudia. mfano: 13-04-2023'
        elif language == "EN":
            message =  "only valid date required here. e.g: 13-04-2023"

        #response    
        return {'error': True, 'message': message}


def validate_past_date(key, language):
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
        past = datetime.strptime(key, "%d/%m/%Y")
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








