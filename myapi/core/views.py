import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from myapi.core import serializers
from rest_framework.permissions import IsAuthenticated  # <-- Here


import json
import requests



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
    def enviarMensaje(self, sender, message):
        payload = { "messaging_product": "whatsapp", "to": f"{sender}","text": {"body": f"{message}"}}
        with requests.Session() as session:
            session.get("https://graph.facebook.com/v13.0/101103879273415/messages")
            r = session.post('https://graph.facebook.com/v13.0/101103879273415/messages', data=json.dumps(payload),
                headers={"Accept": "application/json", "Content-Type": "application/json", 'Authorization': 'Bearer EAAOOyC0ZBmdcBAPntgY9ZBiIhLXnvc29TNP3fRKGs17Hf46KFeQS7gR3lk9gfTY5RnYtZAphVOyTdYMYqPdJbZBhXT4LgMS8ed9lweNJcuwDVelatDVPDsPCZAWGPbqnTcUDdmqPQ0WwsR67Yuv568cdvP9OuIESdT5aFrCRgcFsC69iKi12SoMmhnzWDW6xhZB05m0CKd2gZDZD'})
            print(r.content) 
        return Response({'message': message}, status=status.HTTP_200_OK)
    
    def enviarTemplate(self, message):
        payload = { "messaging_product": "whatsapp","to": "527331258324", "type": "template","template": { "name": "defi_verification", "language": { "code": "es_MX" }} }
        with requests.Session() as session:
            session.get("https://graph.facebook.com/v13.0/101103879273415/messages")
            r = session.post('https://graph.facebook.com/v13.0/101103879273415/messages', data=json.dumps(payload),
                headers={"Accept": "application/json", "Content-Type": "application/json", 'Authorization': 'Bearer EAAOOyC0ZBmdcBAPntgY9ZBiIhLXnvc29TNP3fRKGs17Hf46KFeQS7gR3lk9gfTY5RnYtZAphVOyTdYMYqPdJbZBhXT4LgMS8ed9lweNJcuwDVelatDVPDsPCZAWGPbqnTcUDdmqPQ0WwsR67Yuv568cdvP9OuIESdT5aFrCRgcFsC69iKi12SoMmhnzWDW6xhZB05m0CKd2gZDZD'})
        return Response({'message': message}, status=status.HTTP_200_OK)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try: 
                message = request.data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                sender =  request.data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                name = request.data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                """message = f'Hello {name}!'"""
                if(message == 'Hola'):
                    self.enviarMensaje(sender, 'Vamos por p')
                return Response({'message': message}, status=status.HTTP_200_OK)
            except:
                return Response({'message': "Petición repetida"}, status=status.HTTP_200_OK)
        else: 
            print('la petición tiene errores')
            return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
            )
            