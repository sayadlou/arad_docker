from captcha.fields import BaseCaptchaTextInput, CaptchaTextInput
from django.forms import MultiWidget


# class BaseCaptchaTextInput(MultiWidget):
#     pass



class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'account/custom_field.html'
