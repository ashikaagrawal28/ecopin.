import requests
import os

recaptcha_secret = os.getenv('RECAPTCHA_SECRET_KEY')

class RecaptchaFunc:
    def validate_recaptcha(recaptcha_response):
        payload = {'secret': recaptcha_secret, 'response': recaptcha_response}
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        return r.json().get('success', False)