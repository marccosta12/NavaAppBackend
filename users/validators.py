import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PinPasswordValidator:
    """
    Validador de contraseñas tipo PIN (exactamente 6 dígitos numéricos).
    """
    def validate(self, password, user=None):
        if not re.fullmatch(r"\d{6}", password):
            raise ValidationError(
                _("Password must be a 6-digit numeric PIN."),
                code="invalid_pin",
            )

    def get_help_text(self):
        return _("Your password must be a 6-digit numeric PIN.")
