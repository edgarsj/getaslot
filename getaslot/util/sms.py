import urllib  
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