import urllib  
#import urllib2 

from django.conf import settings

def send_sms(reciever, msg):  
  
    api_url = 'https://messente.com/api/send_sms_get'  
    values = {'user' : settings.MESSENTE_USERNAME,  
            'api_key' : settings.MESSENTE_API_KEY,  
            'text' : msg,  
            'to' : reciever}  
    
    data = urllib.urlencode(values)  
    api_url = api_url + '?' + data  
    data = urllib.urlopen(api_url).read()  
    #print data  