import re

def parse_details(details):
    parsed_data = {
        "date_of_birth": None,
        "date_of_death": None,
        "ethnicity": None,
        "hometown": None,
        "date_entered_party": None,
        "date_entered_party_official": None,
        "expertise": None,
        "degree_education": None,
        "political_theory": None,
        "foreign_language": None,
        "position": None,
        "position_process": None
    }

    # Example patterns (adjust if necessary to match actual content)
    date_of_birth_match = re.search(r"Ngày sinh\s*(.*)", details)
    date_of_death_match = re.search(r"Ngày mất\s*(.*)", details)
    ethnicity_match = re.search(r"Dân tộc\s*(.*)", details)
    hometown_match = re.search(r"Quê quán\s*(.*)", details)
    date_entered_party_match = re.search(r"Ngày vào Đảng\s*(.*)", details)
    date_entered_party_official_match = re.search(r"Ngày chính thức\s*(.*)", details)
    expertise_match = re.search(r"Chuyên môn\s*(.*)", details)
    degree_education_match = re.search(r"Học hàm\s*(.*)", details)
    political_theory_match = re.search(r"Lý luận chính trị\s*(.*)", details)
    foreign_language_match = re.search(r"Ngoại ngữ\s*(.*)", details)
    position_match = re.search(r"Chức vụ\s*(.*)", details, re.DOTALL)
    position_process_match = re.search(r"TÓM TẮT QUÁ TRÌNH CÔNG TÁC:\s*(.*)", details, re.DOTALL)

    # Populate parsed_data with extracted values
    if date_of_birth_match:
        parsed_data["date_of_birth"] = date_of_birth_match.group(1).strip()
    if date_of_death_match:
        parsed_data["date_of_death"] = date_of_death_match.group(1).strip()
    if ethnicity_match:
        parsed_data["ethnicity"] = ethnicity_match.group(1).strip()
    if hometown_match:
        parsed_data["hometown"] = hometown_match.group(1).strip()
    if date_entered_party_match:
        parsed_data["date_entered_party"] = date_entered_party_match.group(1).strip()
    if date_entered_party_official_match:
        parsed_data["date_entered_party_official"] = date_entered_party_official_match.group(1).strip()
    if expertise_match:
        parsed_data["expertise"] = expertise_match.group(1).strip()
    if degree_education_match:
        parsed_data["degree_education"] = degree_education_match.group(1).strip()
    if political_theory_match:
        parsed_data["political_theory"] = political_theory_match.group(1).strip()
    if foreign_language_match:
        parsed_data["foreign_language"] = foreign_language_match.group(1).strip()
    if position_match:
        parsed_data["position"] = position_match.group(1).strip()
    if position_process_match:
        parsed_data["position_process"] = position_process_match.group(1).strip()

    return parsed_data
