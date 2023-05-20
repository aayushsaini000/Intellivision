from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


def _make_hash_value(self, user, timestamp):
    login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
    return (
        six.text_type(user.pk)
        + user.password
        + six.text_type(login_timestamp)
        + six.text_type(timestamp)
    )


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    generate token to restore password
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.email)
        )


account_activation_token = AccountActivationTokenGenerator()
