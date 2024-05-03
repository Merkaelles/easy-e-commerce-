#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest


def send_sms(phone, code):
    client = AcsClient('Your ACCESS_KEY_ID', 'Your ACCESS_KEY_SECRET', 'Your registering region like cn-shanghai')
    # // 创建API请求并设置参数
    request = SendSmsRequest()
    request.set_SignName("Your Signature")
    request.set_TemplateCode('Your TemplateCode')
    params = "{\"code\":\"" + str(code) + "\"}"  # 发送的手机验证码格式
    request.set_TemplateParam(params)
    request.set_PhoneNumbers(str(phone))

    try:
        response = client.do_action_with_exception(request)
        response_x = str(response, encoding='utf-8')
        return response_x
    except ServerException as e:
        return e


if __name__ == '__main__':
    result = send_sms('17629073619', '999888')  # You can enter a phone number to try
    print(result)
