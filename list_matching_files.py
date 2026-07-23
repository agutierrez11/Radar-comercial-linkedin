import re

results_file = "search_results.md"

with open(results_file, "r", encoding="utf-8") as f:
    content = f.read()

# Find all occurrences of "### File: `...` | Row: ..."
matches = re.findall(r"### File: `([^`]+)` \| Row: (\d+)", content)

summary = {}
for file_name, row in matches:
    summary[file_name] = summary.get(file_name, 0) + 1

print("Summary of matches found:")
for file_name, count in summary.items():
    print(f" - {file_name}: {count} matching rows")
