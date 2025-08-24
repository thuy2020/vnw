import json
import random
from people.resume_parser import parse_resume_text

# Load full dataset
with open("gov_individuals.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# Take a random sample of 10
sample = random.sample(records, 10)

# Parse and print results
for i, item in enumerate(sample, 1):
    name = item.get("name", "[No Name]")
    resume_text = item.get("resume_text", "")
    parsed = parse_resume_text(resume_text)

    print(f"\n🧾 Sample {i}: {name}")
    print("Fields Extracted:")
    for key, value in parsed.items():
        print(f"  {key}: {value}")
