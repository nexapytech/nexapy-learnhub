from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from .models import Email_Verification
from django.utils import timezone

from django.utils import timezone

class PasswordGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        verification = Email_Verification.objects.create(user=user)
        token = verification.token
        timestamp = verification.timestamp
        is_email_verified = verification.is_email_verified
        full_token = six.text_type(f'{token}{user.pk}{timestamp}{is_email_verified}')
        verification.full_token = full_token
        verification.save()
        return verification.full_token


generate_token = PasswordGenerator()



class Resend_Verification_Link(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        verification = Email_Verification.objects.get(user=user)
        verification.delete()
        new_verification= Email_Verification.objects.create(user=user)
        token = new_verification.token
        timestamp = new_verification.timestamp
        is_email_verified = new_verification.is_email_verified
        full_token = six.text_type(f'{token}{user.pk}{timestamp}{is_email_verified}')
        new_verification.full_token = full_token
        new_verification.save()

        return full_token




resend_verfication = Resend_Verification_Link()




