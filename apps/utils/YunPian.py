import requests
import json


# def send_verify_sms(api_key, code, mobile):
#     url = "https://sms.yunpian.com/v2/sms/single_send.json"
#     text = "{}".format(code)
#
#     res = requests.post(url, data={
#         "api_key": api_key,
#         "mobile": mobile,
#         "text": text
#     })
#     res_json = json.loads(res.text)
#     return res_json

def send_verify_sms():
    re_json = {
        "code": 0,
        "msg": '',
    }
    return re_json


