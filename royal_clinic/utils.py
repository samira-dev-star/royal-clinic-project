import random

def random_code_generatore(number_of_digits):
    number_of_digits-=1
    return random.randint(10**number_of_digits,10**(number_of_digits+1)-1)

# --------------------------------------------------------------------------------------

from kavenegar import *

def send_sms(mobile_number,message):
    try:
        api = KavenegarAPI('483767334945725152636B334364666167317839484A6361676D48434159446962596A4F334F522F6154593D')
        params = {'sender' : '' , 'receptor' : mobile_number , 'message' : message}
        response = api.sms_send(params)
        return response
    except APIException as error:
        print(f'error1:{error}')
    except HTTPException as error:
        print(f'error2:{error}')
        
        
# --------------------------------------------------------------------------------------
