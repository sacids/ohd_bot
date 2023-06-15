import os
import json
import requests
import logging
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class WhatsAppWrapper:
    BASE_API_URL = "https://graph.facebook.com/v17.0/"
    API_TOKEN=config('WHATSAPP_API_TOKEN')
    NUMBER_ID=config('WHATSAPP_NUMBER_ID')

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.BASE_API_URL + self.NUMBER_ID


    def preprocess(self, data):
        """Preprocess data"""
        return data["entry"][0]["changes"][0]["value"]   


    def get_mobile(self, data):
        """get mobile from the data"""
        data = self.preprocess(data)

        if "contacts" in data:
            return data['contacts'][0]['wa_id'] 


    def get_profile_name(self, data):
        """get profile data from the data"""
        data = self.preprocess(data)

        if "contacts" in data:
            return data['contacts'][0]['profile']['name'] 


    def get_message(self, data):
        """get message from the data""" 
        data = self.preprocess(data)

        if 'messages' in data:
            return data['messages'][0]['text']['body']


    def get_interactive_message(self, data):
        """get interactive message """
        data = self.preprocess(data)

        if "messages" in data:
            if "interactive" in data["messages"][0]:
                return data["messages"][0]["interactive"]    


    def get_location(self, data):
        """get location from the data"""
        data = self.preprocess(data)

        if "messages" in data:
            if "location" in data["messages"][0]:
                return data["messages"][0]["location"]


    def get_image(self, data):
        """get image from the data"""
        data = self.preprocess(data)

        if "messages" in data:
            if "image" in data["messages"][0]:
                return data["messages"][0]["image"]


    def get_document(self, data):
        """get document from the data"""
        data = self.preprocess(data)

        if "messages" in data:
            if "document" in data["messages"][0]:
                return data["messages"][0]["document"]


    def get_audio(self, data):
        """get audio from the data"""
        data = self.preprocess(data)

        if "messages" in data:
            if "audio" in data["messages"][0]:
                return data["messages"][0]["audio"]


    def get_video(self, data):
        """get video from the data"""
        data = self.preprocess(data)

        if "messages" in data:
            if "video" in data["messages"][0]:
                return data["messages"][0]["video"]


    def query_media_url(self, media_id):
        """Query media url from media id"""
        response = requests.get(f"{self.BASE_API_URL}{media_id}", headers=self.headers)

        if response.status_code == 200:
            fileURL = response.json()["url"]

            """return URL"""
            return fileURL
        return None


    def download_media(self, media_url, mime_type, file_name="lainaFile"):
        """Download media from media url"""
        request = requests.get(media_url, headers=self.headers)
        content = request.content
        extension = mime_type.split("/")[1]

        # create a temporary file
        try:
            file_path = os.path.join('/assets/uploads/', f"{file_name}.{extension}")

            #open 
            with open(file_path, "wb") as f:
                f.write(content)
            return f.name
        except Exception as e:
            print(e)
            return None


    def get_messageId(self, data):
        """get message id from data"""
        data = self.preprocess(data) 

        if 'messages' in data:
            return data['messages'][0]['id']  


    def get_message_timestamp(self, data):
        """get message timestamp from data"""
        data = self.preprocess(data) 

        if 'messages' in data:
            return data['messages'][0]['timestamp']                  


    def get_message_type(self, data):
        """get message type from data"""
        data = self.preprocess(data) 

        if 'messages' in data:
            return data['messages'][0]['type']  


    def get_delivery(self, data):
        """get message type from data"""
        data = self.preprocess(data) 

        if 'statuses' in data:
            return data['statuses'][0]['status']              


    def structure_response(self, from_number, message_type, language, message, attachment, arr_trees, main_thread):
        """Structure response """
        message = message.replace("<br>", '\n')

        if message_type == "TEXT":
            sub_message = ""
            for val in arr_trees:
                sub_message += "*" + str(val['view_id']) + "*" + ". " + val['title'] + "\r\n"

            if sub_message != "":  
                message = message + "\n\n" + sub_message

            #TODO: check for back to MAIN MENU
            if main_thread == True:
                back_msg = ""
                if language == "SW":
                    back_msg = "_Andika *0* kurudi ⬅️ *Menyu kuu*_"
                elif language == "EN":
                    back_msg = "_Reply *0* - to go ⬅️ to the *Main Menu*_"

                message = message + "\n\n" + back_msg

            #send text message now
            response = self.send_text_message(from_number, message)

            #check for document attachment
            if attachment is not None:
                response_1 = self.send_document(from_number, attachment, "Ngao Ya Buku - Fomu ya madai")

        elif message_type == "DOCUMENT":
            pass
        elif message_type == "IMAGE":
            pass
        elif message_type == "AUDIO":
            pass
        elif message_type == "VIDEO":
            pass
        elif message_type == "CONTACT":
            pass
        elif message_type == "LOCATION":
            pass
        elif message_type == "LIST MESSAGE":
            #create list format
            arr_data = []
            for val in arr_trees:
                data = {
                        "id":val['view_id'],
                        "title": val['title']           
                    }
                arr_data.append(data)

            #change button message based on language
            if language == "SW":
                buttonTXT = "Chagua kwenye Orodha " 
            elif language == "EN":
                buttonTXT = "Select from Lists" 

            #array new data
            new_arr_data = {
                "button": buttonTXT,
                "sections": [
                    {
                        "title" : "Laina Finance",
                        "rows": arr_data
                    }
                ]
            }

            #TODO: check for back to MAIN MENU
            if main_thread == True:
                back_msg = ""
                if language == "SW":
                    back_msg = "_Andika *0* kurudi ⬅️ *Menyu kuu*_"
                elif language == "EN":
                    back_msg = "_Reply *0* - to go ⬅️ to the *Main Menu*_"

                message = message + "\n\n" + back_msg

            #send list message 
            response = self.send_interactive_message(from_number, "list", message, new_arr_data)   
        elif message_type == "REPLY BUTTON":
            #create button format
            arr_data = []
            for val in arr_trees:
                data = {
                    "type": "reply",
                    "reply": {
                      "id": val['view_id'],
                      "title": val['title']  
                    }      
                }
                arr_data.append(data)

            #array new data
            new_arr_data = {
                "buttons": arr_data
            }

            #TODO: check for back to MAIN MENU
            if main_thread == True:
                back_msg = ""
                if language == "SW":
                    back_msg = "_Andika *0* kurudi ⬅️ *Menyu kuu*_"
                elif language == "EN":
                    back_msg = "_Reply *0* - to go ⬅️ to the *Main Menu*_"

                message = message + "\n\n" + back_msg

            #send button message
            response = self.send_interactive_message(from_number, 'button', message, new_arr_data)

        #return response
        return response


    def send_template_message(self, template_name, language_code, phone_number):
        """Send templete message """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        logging.info(response.json())

        """return response"""
        return response

    def send_text_message(self, phone_number, message):
        """Send text message """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message
            }
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        logging.info(response.json())

        """return response"""
        return response
    

    def send_location(self, phone_number, latitude, longitude, name, address):
        """Send Location """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "location",
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "name": name,
                "address": address,
            },
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        logging.info(response.json())

        """return response"""
        return response
    

    def send_audio(self, phone_number, audioURL):
        """Send Audio """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "audio",
                "audio": {"link": audioURL},
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        logging.info(response.json())

        """return response"""
        return response
    

    def send_video(self, phone_number, videoURL, caption):
        """: Send video """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "video",
                "video": {"link": videoURL, "caption": caption},
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        logging.info(response.json())

        """return response"""
        return response
    

    def send_document(self, phone_number, documentURL, caption):
        """Send document """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "document",
                "document": {"link": documentURL, "caption": caption, "filename": "Ngao_Ya_Buku.pdf"},
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        logging.info(response.json())

        """return response"""
        return response


    def send_interactive_message(self, phone_number, message_type, body, actions):
        """Send interactive message"""
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "interactive",
            "interactive":{
                "type": message_type,
                "body": {
                    "text": body
                },
                "action": actions
            }
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        logging.info(response.json())

        """return response"""
        return response
