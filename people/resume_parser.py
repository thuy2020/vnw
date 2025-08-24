import re
from django.db import models

def parse_resume_text(text):
    if not text or not isinstance(text, str):
        return {}
    data = {}

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
    # ✅ Extract position_process and structured position_history
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

        data["position_history"] = unique_history

    return data
