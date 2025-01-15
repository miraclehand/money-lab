# 한글 초성, 중성, 종성 리스트
F = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
     'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
     'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
S = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ',
     'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ',
     'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
T = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
     'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
     'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
     'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def disassemble_hangul(value):
    """
    한글 문자열을 초성, 중성, 종성으로 분리합니다.
    """
    if not value:
        return ''

    result = []
    for char in value:
        uni = ord(char)

        # 한글 범위 확인
        if 44032 <= uni <= 55203:
            uni -= 44032
            final = uni % 28  # 종성
            medial = ((uni - final) // 28) % 21  # 중성
            initial = (((uni - final) // 28) - medial) // 21  # 초성
            result.append(F[initial] + S[medial] + T[final])
        else:
            result.append(char)

    return ''.join(result)

