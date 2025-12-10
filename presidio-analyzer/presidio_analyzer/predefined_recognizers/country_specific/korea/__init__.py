"""Korea-specific recognizers."""

from .kr_rrn_recognizer import KrRrnRecognizer
from .kr_account_recognizer import KrAccountNumberRecognizer
from .kr_driver_license_recognizer import KrDriverLicenseRecognizer
from .kr_phone_number import KrPhoneNumberRecognizer
from .kr_passport_recognizer import KrPassportRecognizer

__all__ = [
    "KrRrnRecognizer",
    "KrAccountNumberRecognizer",
    "KrDriverLicenseRecognizer",
    "KrPhoneNumberRecognizer",
    "KrPassportRecognizer",
]
