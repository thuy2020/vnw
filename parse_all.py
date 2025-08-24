import json
from people.resume_parser import parse_resume_text

input_file = "gov_individuals.json"
output_file = "clean_individuals.json"

with open(input_file, "r", encoding="utf-8") as f:
    records = json.load(f)
    

cleaned = []
for i, item in enumerate(records):
    resume_text = item.get("resume_text", "")
    parsed = parse_resume_text(resume_text)
    item.update(parsed)
    cleaned.append(item)

    if i % 50 == 0:
        print(f"Processed {i+1}/{len(records)}")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"\n✅ Saved cleaned data to {output_file}")