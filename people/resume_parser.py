import re
from django.db import models

def parse_resume_text(text):
    if not text or not isinstance(text, str):
        return {}
    data = {}

    # Strip honorifics and infer gender if present
    name_match = re.match(r"(Ông|Bà)\s+([A-ZÀ-Ý][^\d:;,]*)", text.strip(), re.IGNORECASE)
    if name_match:
        honorific = name_match.group(1).strip().lower()
        name = name_match.group(2).strip()
        data["name"] = name
        if "gender" not in data or not data["gender"]:
            if honorific == "ông":
                data["gender"] = "Nam"
            elif honorific == "bà":
                data["gender"] = "Nữ"

    def extract(pattern, group=1):
        match = re.search(pattern, text, re.IGNORECASE)
        try:
            return match.group(group).strip()
        except (AttributeError, IndexError):
            return None

    # Normalize line breaks and whitespace
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # -----------------------------
    # ✅ Extract multiple positions under the name
    # -----------------------------
    lines = text.strip().split('. ')
    positions = []
    found_name = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not found_name:
            if line.upper().startswith("ĐỒNG CHÍ") or re.match(r"^[A-Z\s\-ĐỒNG CHÍ]+$", line):
                found_name = True
            continue
        if re.search(r"(Ngày sinh|Nam/Nữ|Dân tộc|Quê quán|Ngày vào Đảng)", line, re.IGNORECASE):
            break
        positions.append(line)

    data["positions"] = positions

    # -----------------------------
    # ✅ Extract other fields
    # -----------------------------
    #gender is only extracted from the text if not already inferred from the honorific.
    if not data.get('gender'):
        data['gender'] = extract(r"Nam/Nữ\s*[:\-]?\s*(Nam|Nữ)")
    data['date_of_birth'] = extract(r"Ngày\s*sinh\s*[:\-]?\s*([\d/]+)")
    data['ethnicity'] = extract(r"Dân\s*tộc\s*[:\-]?\s*([A-Za-zÀ-ỹ\s]+)")

    hometown_match = re.search(
        r"Quê\s*quán\s*[:\-]?\s*(.*?)(?:\-|\.|Ngày|Nam/Nữ|Dân tộc|Chuyên môn|Trình độ|Học vị|Ngoại ngữ|\Z)",
        text,
        re.IGNORECASE
    )
    if hometown_match:
        data['hometown'] = hometown_match.group(1).strip()

    # Extract province from hometown (after 'tỉnh' or 'thành phố')
    hometown_text = data.get("hometown", "")
    province_match = None

    # Prefer province after "tỉnh"
    match_tinh = re.search(r"tỉnh\s*[\n\s]*([A-ZÀ-Ỹ][a-zà-ỹ\s]*)", hometown_text, re.IGNORECASE)
    if match_tinh:
        province_match = match_tinh
    else:
        match_tp = re.search(r"thành phố\s*[\n\s]*([A-ZÀ-Ỹ][a-zà-ỹ\s]*)", hometown_text, re.IGNORECASE)
        if match_tp:
            province_match = match_tp

    if province_match:
        data["hometown_province"] = province_match.group(1).strip()


    # Extract only education title (e.g., Tiến sỹ, Cử nhân, etc.)
    education_match = re.search(r"(Giáo sư|Phó Giáo sư|Tiến sỹ|Thạc sỹ|Cử nhân)", text, re.IGNORECASE)
    if education_match:
        data['education'] = education_match.group(1).strip().title()

    # Attempt to extract school name separately (if exists in resume text)
    school_match = re.search(r"(?:tại|ở)\s+(Trường\s+[^.,;]+)", text, re.IGNORECASE)
    if school_match:
        data['school_name'] = school_match.group(1).strip()

    data['foreign_language'] = extract(r"(?:Ngoại\s*ngữ|Ngôn\s*ngữ)\s*[:\-]?\s*([^\n\-–\.;]+)")
    data['political_theory'] = extract(r"Lý\s*luận\s*chính\s*trị\s*[:\-]?\s*([^\n\-–\.;]+)")
    data['date_entered_party'] = extract(r"Ngày\s*vào\s*Đảng\s*[:\-]?\s*([\d/]+)")
    data['date_entered_party_official'] = extract(r"Ngày\s*chính\s*thức\s*[:\-]?\s*([\d/]+)")

    # -----------------------------
    # ✅ Extract position_process --> produce position_history
    # -----------------------------
    position_history = []
    process_match = re.search(r"(TÓM TẮT\s*)?QUÁ TRÌNH CÔNG TÁC.*?(?=\n|$)", text, re.IGNORECASE)
    if process_match:
        process_text = process_match.group(0).strip()
        data["position_process"] = process_text

        # Extract clean date-range entries
        pattern = re.compile(
            r"(?P<start>\d{1,2}/\d{4})\s*[-–]\s*(?P<end>\d{1,2}/\d{4}|nay|n[aă]y|hiện nay)?[:\-]?\s*(?P<title>[^.]+?)(?=(?:\d{1,2}/\d{4}\s*[-–])|\Z)",
            re.IGNORECASE
        )

        for match in pattern.finditer(process_text):
            start = match.group("start")
            end = match.group("end") or ""
            end = "" if re.match(r"n[aă]y|hiện nay", end, re.IGNORECASE) else end
            title = re.sub(r"\s+", " ", match.group("title")).strip(" :.-;")

            position_history.append({
                "start": start,
                "end": end,
                "title": title
            })

        # Deduplicate by title and overlapping dates
        seen = set()
        unique_history = []
        for item in position_history:
            start = item["start"].strip()
            end = item["end"].strip()
            title = re.sub(r"\s+", " ", item["title"].lower()).strip(" :.-;")
            key = (start, end, title)

            if key in seen:
                continue

            # Avoid overlaps with same title
            overlap = False
            for u in unique_history:
                t2 = re.sub(r"\s+", " ", u["title"].lower()).strip(" :.-;")
                if title == t2:
                    if start == u["start"] or end == u["end"] or start == u["end"] or end == u["start"]:
                        overlap = True
                        break
            if not overlap:
                seen.add(key)
                unique_history.append(item)

        for item in unique_history:
            full_title = item["title"]
            parts = [p.strip() for p in full_title.split(",") if p.strip()]
            if len(parts) > 1:
                item["position"] = ", ".join(parts[:-1])
                item["organizations"] = parts[-1]
            else:
                item["position"] = full_title
                item["organizations"] = None
            # Clean up organization names by removing common job-title phrases
            if item["organizations"]:
                item["organizations"] = re.sub(
                    r"^(Phó Giám đốc|Giám đốc|Chủ tịch|Phó Chủ tịch|Phó Bí thư|Phó Chủ nhiệm|Uỷ viên|Bộ trưởng)\s+", "",
                    item["organizations"],
                    flags=re.IGNORECASE
                ).strip()

        data["position_history"] = unique_history

    return data

def parse_position_history(text):
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    position_history = []
    lines = re.split(r'\.\s*', text)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(
            r"(?P<start>\d{1,2}/\d{4}|\d{4})\s*(?:-|\–|đến)?\s*(?P<end>\d{1,2}/\d{4}|\d{4}|nay)?[:\-]?\s*(?P<title>.+)",
            line)
        if match:
            start = match.group("start")
            end = match.group("end") or None
            title = match.group("title").strip()
            position_history.append({
                "title": title,
                "start": start,
                "end": end
            })
        else:
            # fallback if no match (try to salvage title)
            if len(line) > 10:
                position_history.append({
                    "title": line,
                    "start": None,
                    "end": None
                })
    return position_history


def safe_parse_resume(resume_text, position_process=None, name=None):
    from .resume_parser import parse_resume_text, parse_position_history

    try:
        parsed = parse_resume_text(resume_text or "")
        if not parsed.get("position_history") and position_process:
            print(f"ℹ️ Trying to parse position_process for {name}")
            parsed["position_history"] = parse_position_history(position_process)
        return parsed
    except Exception as e:
        print(f"⚠️ Resume parsing failed for {name}: {e}")
        return {"position_history": []}

#test one example
# if __name__ == "__main__":
#    sample_text = "Ông NGUYỄN VĂN A. Ngày sinh: 01/01/1970. Nam/Nữ: Nam. Dân tộc: Kinh. Quê quán: Xã Quế Phú, huyện Quế Sơn, tỉnh Quảng Nam. Trình độ: Tiến sỹ."
#    result = parse_resume_text(sample_text)
#    from pprint import pprint
# pprint(result)