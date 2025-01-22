from bs4 import BeautifulSoup

def extract_between_markers(text: str, start_tag: str, end_tag: str) -> str:
    start = text.find(start_tag) + len(start_tag)
    end = start + text[start:].find(end_tag)
    return text[start:end].strip()

def remove_number_and_dot(text: str) -> str:
    result = ""
    start_idx = 0

    for i, char in enumerate(text):
        if not (char.isdigit() or char in ('.', ' ')):
            start_idx = i
            break
    return text[start_idx:]

def extract_value_from_html(html_string: str, key: str) -> str:
    try:
        soup = BeautifulSoup(html_string, 'html.parser')
        target_key = remove_number_and_dot(key)
        for tr in soup.find_all('tr'):
            td_elements = tr.find_all('td')
            if len(td_elements) < 2:
                continue
            key_text = td_elements[0].find('span').text.strip()
            if target_key == remove_number_and_dot(key_text):
                return td_elements[1].find('span').text.strip()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
