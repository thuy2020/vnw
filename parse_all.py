import json
from people.resume_parser import safe_parse_resume, parse_position_history

input_file = "gov_individuals.json"
output_file = "clean_individuals.json"

with open(input_file, "r", encoding="utf-8") as f:
    records = json.load(f)


cleaned = []
for i, item in enumerate(records):
    resume_text = item.get("resume_text", "")
    parsed = safe_parse_resume(resume_text)
    item.update(parsed)

    # Fallback: if position_history is missing but position_process exists, try parsing it
    if not item.get("position_history") and item.get("position_process"):
        print(f"ℹ️ Trying to parse position_process for {item.get('name')}")
        try:
            from people.resume_parser import parse_position_history  # ensure fallback parser is used
            item["position_history"] = parse_position_history(item["position_process"])
        except Exception as e:
            print(f"⚠️ Failed to parse position_process for {item.get('name')}: {e}")

    cleaned.append(item)

    if i % 50 == 0:
        print(f"Processed {i+1}/{len(records)}")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"\n✅ Saved cleaned data to {output_file}")