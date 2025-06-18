import re

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

    data["positions"] = positions[:10]

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

    data['education'] = extract(r"(Chuyên môn, nghiệp vụ|Trình độ chuyên môn|Học vị)\s*[:\-]?\s*(.+)")
    data['foreign_language'] = extract(r"Ngoại\s*ngữ\s*[:\-]?\s*(.+)") or extract(r"Ngôn\s*ngữ\s*[:\-]?\s*(.+)")
    data['political_theory'] = extract(r"Lý\s*luận\s*chính\s*trị\s*[:\-]?\s*(.+)")
    data['date_entered_party'] = extract(r"Ngày\s*vào\s*Đảng\s*[:\-]?\s*([\d/]+)")
    data['date_entered_party_official'] = extract(r"Ngày\s*chính\s*thức\s*[:\-]?\s*([\d/]+)")

    # -----------------------------
    # ✅ Extract position_process and structured position_history
    # -----------------------------
    position_history = []
    process_match = re.search(r"TÓM TẮT QUÁ TRÌNH CÔNG TÁC(.*)", text, re.DOTALL | re.IGNORECASE)
    if process_match:
        process_text = process_match.group(1).strip()
        data["position_process"] = process_text

        # Use re.findall to get all date ranges and following text
        pattern = re.compile(r"(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4}|đến nay|hiện nay)[\s:]*([^\d]{5,}?)(?=\d{1,2}/\d{4}\s*[-–]|$)", re.IGNORECASE)
        matches = pattern.findall(process_text)

        for start, end, title in matches:
            clean_title = re.sub(r"\s+", " ", title).strip(" :.-;")
            position_history.append({
                "start": start,
                "end": end,
                "title": clean_title
            })

        data["position_history"] = position_history

    return data
