from typing import List, Optional, Tuple, Union

from presidio_analyzer import EntityRecognizer, Pattern, PatternRecognizer

class KrAccountNumberRecognizer(PatternRecognizer):
    """
    Recognize Korean Account Number.
    
    KB Bank Account Number Formats:
    - Old format: XXX-YY-ZZZZ-ZZC
    - Current format: XXXXYY-ZZ-ZZZZZC
    - Subject code(YY): 01(savings/treasury), 02(savings), 24(free savings), 05(household checking), 04(checking), 25(corporate free), 26(linked)
    
    Hana Bank:
    - Format: XXX-ZZZZZZ-ZZCYY
    - Subject code(YY): 05(savings), 07(savings), 08(free savings), 02(household checking), 01(checking), 04(corporate free), 94(linked)
    
    NH Bank:
    - Format 11-12 digits: XXX(X)-YY-ZZZZZC
    - Format 13 digits: YYY-ZZZZ-ZZZZ-CT
    - Subject code(YY): 01(savings), 02(savings), 12(free savings), 06(household checking), 05(checking), 17(corporate free)
    - For 13-digit format, prefix with 3 to make 3-digit subject code (301, 302, 312, 306, 305, 317)
    
    Shinhan Bank:
    - Format: YYY-ZZZ-ZZZZZC
    - Subject code(YYY): 
      - 100~109, 160, 161 (savings)
      - 110~139 (savings)
      - 140~149 (corporate free)
      - 150~154 (checking)
      - 155~159 (household checking)
    """

    PATTERNS = [
        Pattern(
            "KB Bank Account Number - Old Format",
            r"(?<![0-9])\d{3}[- ](?:0[124]|0[25]|24|25|26)[- ]\d{4}[- ]\d{2,3}(?![0-9])",
            0.1,
        ),
        Pattern(
            "KB Bank Account Number - Current Format",
            r"(?<![0-9])\d{4}(?:0[124]|0[25]|24|25|26)[- ]\d{2}[- ]\d{5,6}(?![0-9])",
            0.1,
        ),
        Pattern(
            "Hana Bank Account Number",
            r"(?<![0-9])\d{3}[- ]\d{6}[- ]\d{2}(?:0[124578]|94)(?![0-9])",
            0.1,
        ),
        Pattern(
            "NH Bank Account Number - 11-12 digits",
            r"(?<![0-9])\d{3,4}[- ](?:0[125]|02|06|12|17)[- ]\d{5,6}(?![0-9])",
            0.1,
        ),
        Pattern(
            "NH Bank Account Number - 13 digits",
            r"(?<![0-9])(?:30[125]|302|306|312|317)[- ]\d{4}[- ]\d{4}[- ]\d{2}(?![0-9])",
            0.1,
        ),
        Pattern(
            "Shinhan Bank Account Number",
            r"(?<![0-9])(?:10[0-9]|1[1-3][0-9]|14[0-9]|15[0-9]|16[01])[- ]\d{3}[- ]\d{6}(?![0-9])",
            0.1,
        ),
    ]

    CONTEXT = [
        "Korean bank account",
        "Korean account number",
        "KB bank",
        "Hana bank",
        "NH bank",
        "Shinhan bank",
        "국민은행",
        "하나은행",
        "농협은행",
        "신한은행",
        "계좌번호",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "kr",
        supported_entity: str = "KR_BANK_ACCOUNT",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        self.replacement_pairs = replacement_pairs if replacement_pairs else [("-", ""), (" ", "")]

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
    
    def _validate_checksum(self, account_number: str) -> bool | None:
        """
        Validate Korean bank account checksum.
        
        Note: The exact checksum algorithm for Korean bank accounts is not publicly disclosed.
        Without official documentation, accurate validation cannot be implemented.
        
        한국 은행 계좌번호의 체크섬 알고리즘은 비공개입니다.
        """
        return None