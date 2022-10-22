from rest_framework import authentication
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class VerifyTokenAuthentication(authentication.TokenAuthentication):
    keyword = os.getenv('keyword')