# myapp/validators.py

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Check if the password length is less than or equal to 25
        if len(password) > 25:
            raise ValidationError(
                _("Password cannot be more than 25 characters."),
                code='password_too_long',
            )

        # Check if the password contains at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_upper',
            )

        # Check if the password contains at least one digit
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Password must contain at least one numeric digit."),
                code='password_no_digit',
            )

        # Check if the password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter, one numeric digit, and one special character, and must not exceed 25 characters.")
