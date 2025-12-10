from typing import List, Optional, Tuple, Union

from presidio_analyzer import EntityRecognizer, Pattern, PatternRecognizer

class KrDriverLicenseRecognizer(PatternRecognizer):
    """
    Recognize Korean Driver License Number.
    
    https://learn.microsoft.com/en-us/purview/sit-defn-south-korea-drivers-license-number 
    
    Pattern 1:
        - two digits
        - hyphen
        - six digits
        - hyphen
        - two digits

    Pattern 2:
        - 2 digits (allowed digits are 11-26 and 28)
        - hyphen
        - two digits
        - hyphen
        - six digits
        - hyphen
        - two digits
    """

    PATTERNS = [
        Pattern(
            "Driver License Number - Pattern 1",
            r"(?<![0-9])(?:1[1-9]|2[0-6]|28)[- ]\d{6}[- ]\d{2}(?![0-9])",
            0.1,
        ),
        Pattern(
            "Driver License Number - Strict Region",
            r"(?<![0-9])(?:1[1-9]|2[0-6]|28)[- ]\d{2}[- ]\d{6}[- ]\d{2}(?![0-9])",
            0.1,
        ),
    ]

    CONTEXT = [
        "Korean driver license",
        "Korean driver license number",
        "대한민국 운전면허증",
        "운전면허증",
        "driver license",
        "driver license number",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "kr",
        supported_entity: str = "KR_DRIVER_LICENSE",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        self.replacement_pairs = replacement_pairs if replacement_pairs else [("-", "")]

        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

    def validate_result(self, pattern_text: str) -> bool | None:
        
        sanitized_value = EntityRecognizer.sanitize_value(
            pattern_text, self.replacement_pairs
        )
        
        if not sanitized_value.isdigit():
            return False

        return self._validate_checksum(sanitized_value)
    
    def _validate_checksum(self, driver_license: str) -> bool | None:
        """
        Validate Korean driver license checksum.
        
        Note: The exact checksum algorithm for Korean driver licenses is not publicly disclosed.
        Without official documentation, accurate validation cannot be implemented.
        
        """
        return None
        