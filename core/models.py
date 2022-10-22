from django.db import models

# # Create your models here.


class UserModel(models.Model):
    name = models.CharField(max_length=21)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length = 17)
    message_id = models.CharField(max_length = 500,default = None)
    incoming_msg = models.CharField(max_length=500)
    gpt_response = models.CharField(max_length=500)
    
