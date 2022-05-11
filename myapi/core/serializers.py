from rest_framework import serializers
from myapi.core import models

class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=21)

class ContactSerializer(serializers.Serializer): 
    profile = ProfileSerializer()
    wa_id = serializers.CharField(max_length = 23)

class TextSerializer(serializers.Serializer):
    body = serializers.CharField(required=False)

class MessageSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField(format="iso-8601", required=False, read_only=True)
    _from_ = serializers.CharField(max_length=21, required=False)
    _id_ = serializers.CharField(max_length = 50, required=False)
    type = serializers.CharField(allow_blank=True)
    text = TextSerializer()

class MetadataSerializer():
    display_phone_number = serializers.CharField(max_length = 17, required=False)
    phone_number_id = serializers.CharField(max_length = 23, required=False)

class ValueSerializer():
    messaging_product = serializers.CharField(required=False)
    metadata = MetadataSerializer()
    contacts = ContactSerializer()
    messages = MessageSerializer(many=True)
    

class ChangesSerializer():
    value = ValueSerializer()
    field = serializers.CharField(max_length = 23)
   

class EntrySerializer(serializers.Serializer):
    _id_ = serializers.CharField(max_length = 23, required=False)
    changes = ChangesSerializer()


class BotSerializer(serializers.Serializer):
    """Serializes the fields of botmaker requests"""
    object = serializers.CharField()
    entry = EntrySerializer(many=True)
    

"""
    messaging_product = serializers.CharField(required=False)
    contacts = ContactSerializer(many=True)
   

"""