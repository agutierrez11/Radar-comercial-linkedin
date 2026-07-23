import re

input_file = "clip_posts.txt"
output_file = "clip_posts_filtered.txt"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Split by the separator used in clip_posts.txt (let's assume it has a hyphen-based or line-based format)
# Let's inspect the file structure
print("Reading clip_posts.txt...")
lines = content.splitlines()
print(f"Total lines: {len(lines)}")

# Let's write a script to display posts that contain numbers, achievements, congrats, or team celebrations.
# Keywords: 'podio', 'meta', 'cumplimiento', 'cuota', 'récord', 'top', 'performance', 'ranking', 'ganamos', 'cerrando', 'mes'
keywords = [
    r"podio", r"podium", r"meta", r"cuota", r"cumpli", r"r[eé]cord", r"top", r"performance",
    r"ranking", r"gan", r"cerr", r"logr", r"orgull", r"reconoc", r"agradec", r"orange", r"naranja"
]
rx = re.compile("|".join(keywords), re.IGNORECASE)

matches = []
current_post = []
post_idx = 0

for line in lines:
    if line.startswith("Row ") or line.startswith("Row:") or "URN:" in line or "https://www.linkedin.com" in line:
        if current_post:
            post_text = "\n".join(current_post)
            if rx.search(post_text):
                matches.append(post_text)
            current_post = []
        current_post.append(line)
    else:
        current_post.append(line)

if current_post:
    post_text = "\n".join(current_post)
    if rx.search(post_text):
        matches.append(post_text)

with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} potential achievement posts out of the Clip posts:\n\n")
    for idx, m in enumerate(matches, start=1):
        out.write(f"--- MATCH {idx} ---\n")
        out.write(m + "\n")
        out.write("=" * 80 + "\n\n")

print(f"Done. Found {len(matches)} matching posts. Written to {output_file}")
