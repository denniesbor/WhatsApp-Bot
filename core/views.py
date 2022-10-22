import re
import os
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from . import serializers
from . import models
from rest_framework.permissions import IsAuthenticated  # <-- Here

from flask import session
import json
import requests


# gpt3 
from . import gpt3
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
Bearer = os.getenv('Bearer')
# regular expression
regexp = re.compile(r'nations?|news')

# get chat log
def get_chat_log(query, sender):
    
    chat_log = ''
    for message in query:
        incoming_msg = message['incoming_msg']
        gpt_response = message['gpt_response']

        chat_log = chat_log + sender.upper() + ': ' + incoming_msg + '\n\n' + 'Dennies Bot: ' + gpt_response +'\n\n'

    return chat_log

class HelloView(APIView):        # <-- And here
    serializer_class = serializers.BotSerializer
    def get(self, request):
        challenge = self.request.query_params.get('hub.challenge')
        if challenge:
            return Response(int(challenge))
        else: 
            return Response("Soy tu amigo Fiel")
    
            
        
class BotViewSet(viewsets.ViewSet):
    serializer_class = serializers.BotSerializer
    requestData = ''
    def list(self, request):
        """Manages the functions of the bot"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial update)',
            'Automatically maps to URLS using Routers', 
            'Provides more functionality with less code'
        ]
        challenge = self.request.query_params.get('hub.challenge')
        if challenge:
            return Response(int(challenge))
        else: 
            return Response({'message': 'Hello!', 'a_viewset': a_viewset})
    def sendMsg(self, sender, message):
        payload = { "messaging_product": "whatsapp", "to": f"{sender}","text": {"body": f"{message}"}}
        with requests.Session() as session:
            session.get("https://graph.facebook.com/v14.0/105361369000085/messages")
            r = session.post('https://graph.facebook.com/v14.0/105361369000085/messages', data=json.dumps(payload),
                headers={"Accept": "application/json", "Content-Type": "application/json", 'Authorization': f'Bearer {Bearer}'})
            # print(r.content) 
        return Response({'message': message}, status=status.HTTP_200_OK)
    
    def msgTemplate(self, sender, message):
        payload = { "messaging_product": "whatsapp","to": f"{sender}", "type": "template","template": { "name": "hello_world", "language": { "code": "en_US" }} }
        with requests.Session() as session:
            session.get("https://graph.facebook.com/v14.0/105361369000085/messages")
            r = session.post('https://graph.facebook.com/v14.0/105361369000085/messages', data=json.dumps(payload),
                headers={"Accept": "application/json", "Content-Type": "application/json", 'Authorization': f'Bearer {Bearer}'})
            # print(r.content)
        return Response({'message': message}, status=status.HTTP_200_OK)

    def sendNews(self, sender):
        files = os.listdir(os.path.join('static','articles'))
        filelink = (sorted([file for file in files if file.endswith('pdf')]))[-1]
        
        payload = { "messaging_product": "whatsapp","recipient_type": "individual","to": f"{sender}", "type": "document","document": { "link": f"https://www.chepkelio.fun/static/articles/{filelink}", "filename": f"{filelink}"} }
        with requests.Session() as session:
            session.get("https://graph.facebook.com/v14.0/105361369000085/messages")
            r = session.post('https://graph.facebook.com/v14.0/105361369000085/messages', data=json.dumps(payload),
                headers={"Accept": "application/json", "Content-Type": "application/json", 'Authorization': f'Bearer {Bearer}'})
            # print(r.content)
        return Response({'message': "articles sent"}, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
   
        if serializer.is_valid():
        
            try: 
                message = request.data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                sender =  request.data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                name = request.data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                wa_id = request.data['entry'][0]['changes'][0]['value']['messages'][0]['id']
                
                # if request.session.has_key("chat_log"):
                #     chat_log = request.session["chat_log"]
                # else:
                #     chat_log = request.session.get('chat_log',None)
        
                queryset = models.UserModel.objects.filter(
                    sender = sender).order_by('timestamp').values('incoming_msg','gpt_response')
               
                chat_log = get_chat_log(list(queryset)[-5:], name)
                
                greetings = ['hey','denno','bor', 'boss', 'mzee', 'mambo', 'sasa','hello', 'hi', 'oya']
                # check text language
                non_en = True        
                gpt3_response = ''
                
                if message.lower() in greetings:
                    text = """Hey there. How are you? I am Dennies Bot, a GPT-3-based bot integrated with WhatsApp business API running on a Django server. 
                    I am an assistant to my company, 17 AI which deals with AI in aerospace, agriculture, medical, etc., industries. 
                    I can help you with a variety of tasks, including getting news-related information. 
                    Just respond with 'news' or 'nation', and I will send you daily updates from The Nation. 
                    Other news sources, such as The Standard, will be added soon.
                    """
                    gpt3_response = gpt3.ask(text,person=name,chat_log=None)
                    data = {
                        'name': name,
                        'sender': sender,
                        'message_id': wa_id,
                        'incoming_msg': message,
                        'gpt_response': gpt3_response    
                    }
                else:
                    lang = gpt3.get_lang(message)
                    try:
                        assert lang == 'en'
                        print('english language')
                        gpt3_response = gpt3.ask(message,person=name,chat_log=chat_log)
                        print(gpt3_response)
                        non_en = False
                        data = {
                            'name': name,
                            'sender': sender,
                            'message_id': wa_id,
                            'incoming_msg': message,
                            'gpt_response': gpt3_response    
                        }
                    except AssertionError:
                        print('not english')
                        lang_warn = """If you are not speaking English, Dennies Bot will not be able to understand you. 
                        Please switch to English so that Dennies Bot can learn from you.
                        Don't worry, we will eventually incorporate other languages!
                        """
                        non_en = True
                        non_en_resp = gpt3.ask(lang_warn,person=name,chat_log=None)
                        data = {
                                'name': name,
                                'sender': sender,
                                'message_id': wa_id,
                                'incoming_msg': message,
                                'gpt_response': non_en_resp    
                            }
                    
                    serialized_data = serializers.UserSerializer(data=data) 
                    if serialized_data.is_valid():
                        serialized_data.save()
                # save the serialized data
                
                # print(request.session['chat_log'])
                # """message = f'Hello {name}!'"""
                # print(f"'message': '{message}' 'sender': '{sender}' 'send msg': {gpt3_response}")
                message = message.lower()
                print(non_en) 
                if regexp.search(message) and message not in greetings:
                    text = f"""
                    Do you mean the Kenyan Nation Media News? 
                    Well, I got you. 
                    Here is a pdf version of your news as at {datetime.datetime.today().strftime("%H:%M of %d %b %Y")}
                    """
                    gpt3_response = gpt3.ask(text,person=name,chat_log=None)               
                elif(gpt3_response==''):
                    gpt3_response = gpt3.ask('I do not understand that',person=name,chat_log=None)
                
                if regexp.search(message):
                    self.sendMsg(sender,gpt3_response)
                    self.sendNews(sender)
                elif non_en and (message not in greetings):
                    self.sendMsg(sender,non_en_resp)
                else:
                    self.sendMsg(sender,gpt3_response)
                return Response({'message': message}, status=status.HTTP_200_OK)
            except:
                return Response({'message': "Successful"}, status=status.HTTP_200_OK)
        else: 
            print('Error')
            return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
            )
            