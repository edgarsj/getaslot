import urllib  
import datetime

from slots.models import Appointment

#import urllib2 

from django.conf import settings

def send_sms(reciever, msg):  
  
    ss='http://adforte.com/jovi.member.app-user-commands?action=send&user=agris.ameriks@ameri.lv&password=u@m3d-M1ySyV&phone=+37126461101&sender=GetASlot&text=You'
    #api_url = 'https://messente.com/api/send_sms_get'
    #  values = {'user' : settings.MESSENTE_USERNAME,  
#            'api_key' : settings.MESSENTE_API_KEY,  
#            'text' : msg,  
#            'to' : reciever}  
#    
    
    api_url = 'http://adforte.com/jovi.member.app-user-commands'
    values = { 
              'action' : 'send',
              'user' : 'agris.ameriks@ameri.lv',
              'password' : 'u@m3d-M1ySyV',
              'sender' : 'GetASlot',
              'phone' : reciever,
              'text' : msg
              }
    data = urllib.urlencode(values)  
    api_url = api_url + '?' + data  
    data = urllib.urlopen(api_url).read()  
    return data  

def send_confirmations():
    #start_datetime = datetime.datetime.now() - datetime.timedelta(0,600,0)
    obj_list = Appointment.objects.filter(confirmation_sent=False)
    for o in obj_list:
        print o
        if o.phone.startswith('+3712') or (len(o.phone)==8 and o.phone.startswith('2')):
            if len(o.phone) ==8:
                o.phone = '+371'+o.phone
            msg = u'Henry will be waiting for you at Alexandra Beauty on %s at %s' % (
                                o.starttime.strftime(u'%Y-%m-%d'),
                                o.starttime.strftime(u'%H:%M'),
                                )
            
            data = send_sms(o.phone, msg)
        o.confirmation_sent = True
        o.save()