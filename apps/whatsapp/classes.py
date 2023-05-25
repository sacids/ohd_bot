import json
import requests
from django.http import HttpResponse, JsonResponse
from decouple import config
import logging

class WhatsAppWrapper:
    API_URL = "https://graph.facebook.com/v16.0/"
    API_TOKEN=config('WHATSAPP_API_TOKEN')
    NUMBER_ID=config('WHATSAPP_NUMBER_ID')

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID


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
        """Query media url from media id obtained either by manually uploading media or received media"""
        response = requests.get(f"{self.API_URL}/{media_id}", headers=self.headers)

        logging.info("media response")
        logging.info(response.json())

        if response.status_code == 200:
            fileURL = response.json()["url"]

            """return URL"""
            return fileURL
        return None


    def download_media(self, media_url, mime_type, file_path= "temp"):
        """Download media from media url obtained either by manually uploading media or received media"""
        r = requests.get(media_url, headers=self.headers)
        content = r.content
        extension = mime_type.split("/")[1]

        # create a temporary file
        try:
            save_file_here = (
                f"{file_path}.{extension}" if file_path else f"temp.{extension}"
            )
            with open(save_file_here, "wb") as f:
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


    def structure_response(self, from_number, message_type, message, arr_trees):
        """__summary__: Structure response """
        if message_type == "TEXT":
            sub_message = ""
            for val in arr_trees:
                sub_message += val['view_id'] + ". " + val['title'] + "\r\n"
            message = message + "\r\n" + sub_message

            #send text message now
            response = self.send_text_message(from_number, message)  
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
                    "title": val['title'],
                    "rows": [
                        {
                            "id":val['view_id'],
                            "title": val['title'],
                            "description": val['description'],           
                        }
                    ]      
                }
                arr_data.append(data)

            #array new data
            new_arr_data = {
                "button": "Bonyeza Hapa",
                "sections": arr_data
            }
            logging.info(new_arr_data)    
 
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
            logging.info(new_arr_data)

            #send button message
            response = self.send_interactive_message(from_number, 'button', message, new_arr_data)

        #return response
        return response


    def send_template_message(self, template_name, language_code, phone_number):
        """__summary__: Send templete message """
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

        """return response"""
        return response

    def send_text_message(self, phone_number, message):
        """__summary__: Send text message """
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

        """return response"""
        return response
    

    def send_location(self, phone_number, latitude, longitude, name, address):
        """__summary__: Send Location """
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

        """return response"""
        return response
    

    def send_audio(self, phone_number, audioURL):
        """__summary__: Send Audio """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "audio",
                "audio": {"link": audioURL},
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        """return response"""
        return response
    

    def send_video(self, phone_number, videoURL, caption):
        """__summary__: Send video """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "video",
                "video": {"link": videoURL, "caption": caption},
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        """return response"""
        return response
    

    def send_document(self, phone_number, documentURL, caption):
        """__summary__: Send document """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "document",
                "document": {"link": documentURL, "caption": caption},
        })

        """response"""
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        """return response"""
        return response


    def send_interactive_message(self, phone_number, message_type, body, actions):
        """__summary__: Send interactive message"""
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

        """return response"""
        return response
