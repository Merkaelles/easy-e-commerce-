import os

# sms发送短信限流参数
LIMIT_SMS_CODE_BY_PHONE = '1/minute'
LIMIT_SMS_CODE_BY_IP = '10/h'
SMS_VERIFY_CODE_EXPIRE = 5 * 60  # 验证码有效5min

SECRET_KEY = os.urandom(16)  # 生成一个随机数密钥
JWT_EXPIRY_SECOND = 60 * 60

