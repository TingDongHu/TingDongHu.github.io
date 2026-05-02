import re

# Read the file
with open(r"F:\Hugo_Blog\my_blog\content\posts\Agent\论文阅读RCL.md", "r", encoding="utf-8") as f:
    content = f.read()

# Replace old image references with new ones
# Remove lines 230-232 (Figure1 and Table2)
content = re.sub(r'\t\t!\[Figure1\]\(论文阅读RCL/image-20260419225358322\.png\)\n\t', '', content)
content = re.sub(r'\t\t!\[Table2\]\(论文阅读RCL/image-20260419225425485\.png\)\n\t', '', content)

# Replace Table3 and Table4 (lines 458-460)
content = re.sub(r'\t\t!\[Table3\]\(论文阅读RCL/image-20260419225509539\.png\)\n\t', '', content)
content = re.sub(r'\t\t!\[Table4\]\(论文阅读RCL/image-20260419225532269\.png\)\n\t', '', content)

# Replace Figure2 and Figure3 (lines 485-487)
content = re.sub(r'\t\t!\[Figure2\]\(论文阅读RCL/image-20260419225653222\.png\)\n\t', '', content)
content = re.sub(r'\t\t!\[Figure3\]\(论文阅读RCL/image-20260419225726367\.png\)\n\t', '', content)

# Write back
with open(r"F:\Hugo_Blog\my_blog\content\posts\Agent\论文阅读RCL.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Replacements completed")
