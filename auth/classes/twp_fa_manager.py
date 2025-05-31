from db.redis import redis_client
import math, random
from shared.functions.send_sms import sendSMS
from shared.functions.sms_templates import smsTemplates


class TwoFactorAuthManager:
    def __init__(self):
        self.prekeyOtp = "2FA_USERID:"
        self.prekeyActivate2FA = "2FA_ACTIVATE_USERID:"
        self.ttl = 120  # seconds

    def _generateOTP(self):
        digits = "0123456789"
        OTP = ""

        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]

        return OTP

    def _deleteOtp(self, key):
        redis_client.delete(key)

    def setOtp(self, userId: int, cellphone: str):
        key = self.prekeyOtp + str(userId)
        value = self._generateOTP()

        sendSMS(cellphone, smsTemplates("2fa", value))

        redis_client.set(key, value, self.ttl)

    def verifyOtp(self, userId: str, otp: str) -> bool:
        key = self.prekeyOtp + str(userId)

        saved_otp = redis_client.get(key)

        result = otp == saved_otp

        if result:
            self._deleteOtp(key)

        return result

    def setActivate2FAOtp(self, userId: int, cellphone: str):
        key = self.prekeyActivate2FA + str(userId)
        value = self._generateOTP()

        sendSMS(cellphone, smsTemplates("activate2fa", value))

        redis_client.set(key, value, self.ttl)

    def verifyActivate2FA(self, userId: str, otp: str) -> bool:
        key = self.prekeyActivate2FA + str(userId)
        saved_otp = redis_client.get(key)

        result = otp == saved_otp

        if result:
            self._deleteOtp(key)

        return result
