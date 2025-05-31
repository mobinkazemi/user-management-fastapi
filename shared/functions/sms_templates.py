from typing import Literal


def smsTemplates(template: Literal["2fa", "activate2fa"], data):
    data = str(data)

    if template == "2fa":
        return f"Your verification code is: {data}"

    elif template == "activate2fa":
        return f"Your 2FA activation code is: {data}"

    return "Invalid template"
