import xml.etree.ElementTree as ET

def extract_between_markers(text: str, start_tag: str, end_tag: str) -> str:
    start = text.find(start_tag) + len(start_tag)
    end = start + text[start:].find(end_tag)
    return text[start:end].strip()

def extract_value_from_xml(xml_string: str, key: str) -> str:
    try:
        root = ET.fromstring(xml_string)
        for tr in root.findall(".//tr"):
            td_elements = tr.findall(".//td")
            if len(td_elements) >= 2:
                key_text = td_elements[0].find("span").text.strip()
                if key in key_text:
                    return td_elements[1].find("span").text.strip()
        return None
    except Exception as e:
        print(f"Error : {e}")
        return None
