import re


def mobile(phone):
    if re.match(r'^1[3-9]\d{9}$', phone):
        return phone
    else:
        raise ValueError(f'{phone} is not a valid mobile')


def email_addr(email):
    if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$', email):
        return email
    else:
        raise ValueError(f'{email} is not a valid email')


def regex(pattern):
    def validate(value):
        if re.match(pattern, value):
            return value
        else:
            raise ValueError(f'{value} is not a valid params')

    return validate
