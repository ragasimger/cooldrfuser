from random import randint
import string
from django.contrib.auth import get_user_model
User = get_user_model()
# from django.core.cache import cache

def rand_letters():
    alphabets = []
    letters = list(string.ascii_letters)
    for _ in range(4):
        rand_int = randint(0,51)
        y = letters[rand_int]
        alphabets.append(y)
    return ''.join(alphabets)

def rand_numbers():
    return randint(1000,999999)

def otp():
    letters = rand_letters()
    nums = str(rand_numbers())
    return letters + nums

otp_ = otp()

def perform_otp_save(email):
    user = User.objects.get(email=email)
    user.otp = otp_
    user.save()
