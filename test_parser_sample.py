import re
from pprint import pprint


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


# Example: paste the `position_process` here
position_process_text = """

TÓM TẮT QUÁ TRÌNH CÔNG TÁC Năm 1996: Cán bộ kinh doanh đối ngoại Chi nhánh Ngân hàng Thương mại Cổ phần Công Thương Việt Nam (VietinBank) Ba Đình. Năm 2000: Thư ký Tổng giám đốc VietinBank. Năm 2003: Thư ký Tổng giám đốc, kiêm Phó Chánh Văn phòng VietinBank. Năm 2006-2009: Phó trưởng phòng, Trưởng phòng Khách hàng doanh nghiệp lớn của VietinBank. 12/2011 - 4/2014: Ủy viên Ban Chấp hành Đảng bộ, Ủy viên Ban Thường vụ Đảng ủy, Ủy viên HĐQT, Tổng Giám đốc VietinBank. 5/2014 - 9/2014: Bí thư Đảng ủy, Chủ tịch HĐQT VietinBank. 9/2014 - 1/2016: Ủy viên Ban Thường vụ Đảng ủy Khối Doanh nghiệp Trung ương; Bí thư Đảng ủy, Chủ tịch HĐQT VietinBank. 1/2016 - 7/2018: Ủy viên dự khuyết Ban Chấp hành Trung ương Đảng khóa XII, Ủy viên Ban Thường vụ Đảng ủy Khối Doanh nghiệp Trung ương; Bí thư Đảng ủy, Chủ tịch HĐQT VietinBank. 7/2018 - 6/2019: Bộ Chính trị luân chuyển, chỉ định tham gia Ban Chấp hành, Ban Thường vụ Tỉnh ủy Quảng Ninh khóa XIV, nhiệm kỳ 2015 - 2020; HĐND tỉnh bầu giữ chức Phó Chủ tịch UBND tỉnh Quảng Ninh khóa XIII, nhiệm kỳ 2016- 2021. 6/2019 - 7/2019: Phó Bí thư Tỉnh ủy khóa XIV, nhiệm kỳ 2015 - 2020; Phó Chủ tịch UBND tỉnh Quảng Ninh khóa XIII, nhiệm kỳ 2016 - 2021. 7/2019 - 10/2020: Phó Bí thư Tỉnh ủy khóa XIV, Chủ tịch UBND tỉnh Quảng Ninh khóa XIII, nhiệm kỳ 2016 - 2021. 14/10/2020: Tại Đại hội đại biểu Đảng bộ tỉnh Điện Biên lần thứ XIV, được bầu giữ chức Bí thư Tỉnh ủy khóa XIV, nhiệm kỳ 2020-2025. 30/1/2021: Tại Đại hội đại biểu toàn quốc lần thứ XIII của Đảng, được bầu làm Ủy viên chính thức Ban Chấp hành Trung ương Đảng khóa XIII, nhiệm kỳ 2021-2026. 10/2022 - 11/2024: Ủy viên Trung ương Đảng, Bộ trưởng Bộ Giao thông vận tải. 11/2024 - nay: Ủy viên Trung ương Đảng, Bộ trưởng Bộ Tài chính . 24/01/2025: Bộ Chính trị chỉ định tham gia Ban Chấp hành Đảng bộ Chính phủ nhiệm kỳ 2020 – 2025.
"""

parsed_positions = parse_position_history(position_process_text)
pprint(parsed_positions)