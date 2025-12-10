from typing import List, Optional, Tuple, Union

from presidio_analyzer import EntityRecognizer, Pattern, PatternRecognizer

class KrPhoneNumberRecognizer(PatternRecognizer):
    """
    Recognize Korean Phone Number.
    
    
    Korean phone numbers can have various formats, including:
    - Mobile numbers: 010-XXXX-YYYY
    - Landline numbers: XXX-YYY(Y)-ZZZZ 
    where XXX is the area code (e.g., 02 for Seoul, 031 for Gyeonggi-do, etc.)
    
    
    Korean Regional Area Codes:
    - 02: 서울특별시 (Seoul)
    - 031: 경기도 (Gyeonggi-do)
    - 032: 인천광역시 (Incheon)
    - 033: 강원특별자치도 (Gangwon)
    - 041: 충청남도 (Chungcheongnam-do)
    - 042: 대전광역시 (Daejeon)
    - 043: 충청북도 (Chungcheongbuk-do)
    - 044: 세종특별자치시 (Sejong)
    - 051: 부산광역시 (Busan)
    - 052: 울산광역시 (Ulsan)
    - 053: 대구광역시 (Daegu)
    - 054: 경상북도 (Gyeongsangbuk-do)
    - 055: 경상남도 (Gyeongsangnam-do)
    - 061: 전라남도 (Jeollanam-do)
    - 062: 광주광역시 (Gwangju)
    - 063: 전북특별자치도 (Jeonbuk)
    - 064: 제주특별자치도 (Jeju)
    
    """

    PATTERNS = [
        Pattern(
            "Phone Number",
            r"(?<![0-9])(010)[- ]\d{3,4}[- ]\d{4}(?![0-9])",
            0.1,
        ),
        Pattern(
            "Landline Number",
            r"(?<![0-9])(02|(03[1-3]|04[1-4]|05[1-5]|06[1-4]))[- ]\d{3,4}[- ]\d{4}(?![0-9])",
            0.1,
        ),
    ]

    CONTEXT = [
        "Korean phone number",
        "Korean phone",
        "대한민국 전화번호",
        "전화번호",
        "phone number",
        "phone",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "kr",
        supported_entity: str = "KR_PHONE_NUMBER",
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