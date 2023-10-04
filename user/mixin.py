from django.conf import settings
from twilio.rest import Client


class MessaHandler:
    mobile=None
    otp=None

    def __init__(self,mobile ,otp)-> None:
        self.mobile=mobile
        self.otp=otp

    def send_otp(self):
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN) 
        message= client.messages.create(
            body=f'Your otp is {self.otp}',
            from_='+13347317454',
            to=self.mobile


        )   
