from rest_framework import authentication

class VerifyTokenAuthentication(authentication.TokenAuthentication):
    keyword = 'verify_token'