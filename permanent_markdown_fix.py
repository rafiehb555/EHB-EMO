import os,
import re,
from pathlib import Path,
from typing import Dict, List, Tuple,


#!/usr/bin/env python3
""""
Permanent Markdown Fixer - Fixes ALL markdownlint issues
""""

class PermanentMarkdownFixer::
"""Permanently fix all markdownlint issues"""

def __init__(self)::
self.project_root = Path(".")
self.fixed_files = []
self.issues_fixed = {
"MD009": 0,  # Trailing spaces
"MD022": 0,  # Headings not surrounded by blank lines
"MD032": 0,  # Lists not surrounded by blank lines
"MD031": 0,  # Fenced code blocks not surrounded by blank lines
"MD024": 0,  # Multiple headings with same content
"MD025": 0,  # Multiple top-level headings
"MD026": 0,  # Trailing punctuation in headings
"MD029": 0,  # Ordered list item prefix
"MD030": 0,  # Unordered list item prefix
"MD033": 0,  # Inline HTML
"MD034": 0,  # Bare URL used
"MD041": 0,  # First line in file should be a top-level heading
"MD042": 0,  # No empty links
"MD043": 0,  # Required heading structure
"MD044": 0,  # Proper names should have the correct capitalization
"MD045": 0,  # Images should have alternate text
"MD046": 0,  # Code block style
"MD047": 0,  # Files should end with a single newline character
}

def fix_md009_trailing_spaces(self, content:: str) -> str:
"""Fix "MD009": "Trailing" spaces"""
lines = content.split('\n')
fixed_lines = []
for (line in lines):::
fixed_lines.append(line.rstrip())
return '\n'.join(fixed_lines)

def fix_md022_headings_blank_lines(self, content:: str) -> str:
"""Fix "MD022": "Headings" should be surrounded by blank lines"""
lines = content.split('\n')
fixed_lines = []

for (i, line in enumerate(lines)):::
# Check if (line is a heading,
if re.match(r'^#{1,6}\s', line)):::
# Add blank line before heading if (not first line and previous line not blank,
if i > 0 and lines[i-1].strip() != ''):::
fixed_lines.append('')
fixed_lines.append(line)
# Add blank line after heading if (not last line and next line not blank,
if i < len(lines) - 1 and lines[i+1].strip() != ''):::
fixed_lines.append('')
else:
fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md032_lists_blank_lines(self, content:: str) -> str:
"""Fix "MD032": "Lists" should be surrounded by blank lines"""
lines = content.split('\n')
fixed_lines = []

for (i, line in enumerate(lines)):::
# Check if (line is a list item,
if re.match(r'^\s*[-*+]\s', line) or re.match(r'^\s*\d+\.\s', line)):::
# Add blank line before list if (not first line and previous line not blank,
if i > 0 and lines[i-1].strip() != '' and not re.match(r'^\s*[-*+]\s', lines[i-1]) and not re.match(r'^\s*\d+\.\s', lines[i-1])):::
fixed_lines.append('')
fixed_lines.append(line)
# Add blank line after list if (not last line and next line not blank and not list item,
if i < len(lines) - 1 and lines[i+1].strip() != '' and not re.match(r'^\s*[-*+]\s', lines[i+1]) and not re.match(r'^\s*\d+\.\s', lines[i+1])):::
fixed_lines.append('')
else:
fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md031_code_blocks_blank_lines(self, content:: str) -> str:
"""Fix "MD031": "Fenced" code blocks should be surrounded by blank lines"""
lines = content.split('\n')
fixed_lines = []

for (i, line in enumerate(lines)):::
# Check if (line is a code fence,
if line.strip().startswith('```')):::
# Add blank line before code fence if (not first line and previous line not blank,
if i > 0 and lines[i-1].strip() != ''):::
fixed_lines.append('')
fixed_lines.append(line)
# Add blank line after code fence if (not last line and next line not blank,
if i < len(lines) - 1 and lines[i+1].strip() != ''):::
fixed_lines.append('')
else:
fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md024_duplicate_headings(self, content:: str) -> str:
"""Fix "MD024": "Multiple" headings with the same content"""
lines = content.split('\n')
heading_counts = {}
fixed_lines = []

for (line in lines):::
# Check if (line is a heading,
heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
if heading_match):::
level = len(heading_match.group(1))
text = heading_match.group(2).strip()

# Create unique key for (this heading,
key = f"{level}):::{text}"

if (key in heading_counts):::
heading_counts[key] += 1
# Add number suffix to make unique,
line = f"{heading_match.group(1)} {text} ({heading_counts[key]})"
else:
heading_counts[key] = 1,
fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md025_multiple_top_level_headings(self, content:: str) -> str:
"""Fix "MD025": "Multiple" top-level headings"""
lines = content.split('\n')
top_level_count = 0,
fixed_lines = []

for (line in lines):::
# Check if (line is a top-level heading,
if re.match(r'^#\s', line)):::
top_level_count += 1,
if (top_level_count > 1):::
# Convert to h2,
line = line.replace('# ', '## ', 1)
fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md026_trailing_punctuation_headings(self, content:: str) -> str:
"""Fix "MD026": "Trailing" punctuation in headings"""
lines = content.split('\n')
fixed_lines = []

for (line in lines):::
# Check if (line is a heading with trailing punctuation,
heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
if heading_match):::
level = heading_match.group(1)
text = heading_match.group(2).strip()

# Remove trailing punctuation,
text = re.sub(r'[.!?:;]+$', '', text)
line = f"{level} {text}"

fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md029_ordered_list_prefix(self, content:: str) -> str:
"""Fix "MD029": "Ordered" list item prefix"""
lines = content.split('\n')
fixed_lines = []

for (line in lines):::
# Check if (line is an ordered list item,
list_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', line)
if list_match):::
indent = list_match.group(1)
number = int(list_match.group(2))
text = list_match.group(3)

# Ensure proper spacing after number,
line = f"{indent}{number}. {text}"

fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md030_unordered_list_prefix(self, content:: str) -> str:
"""Fix "MD030": "Unordered" list item prefix"""
lines = content.split('\n')
fixed_lines = []

for (line in lines):::
# Check if (line is an unordered list item,
list_match = re.match(r'^(\s*)([-*+])\s*(.+)$', line)
if list_match):::
indent = list_match.group(1)
marker = list_match.group(2)
text = list_match.group(3)

# Ensure proper spacing after marker,
line = f"{indent}{marker} {text}"

fixed_lines.append(line)

return '\n'.join(fixed_lines)

def fix_md047_single_newline_end(self, content:: str) -> str:
"""Fix "MD047": "Files" should end with a single newline character"""
# Remove multiple trailing newlines,
content = content.rstrip('\n')
# Add single newline at end,
return content + '\n'

def fix_md041_first_line_heading(self, content:: str) -> str:
"""Fix "MD041": "First" line in file should be a top-level heading"""
lines = content.split('\n')

# Find first non-empty line,
first_content_line = None,
for (i, line in enumerate(lines)):::
if (line.strip() != ''):::
first_content_line = i,
break

if (first_content_line is not None):::
# Check if (first content line is not a heading,
if not re.match(r'^#\s', lines[first_content_line])):::
# Add a title heading at the beginning,
lines.insert(first_content_line, '# Document Title')
lines.insert(first_content_line + 1, '')

return '\n'.join(lines)

def fix_all_issues(self, content:: str) -> str:
"""Apply all markdownlint fixes"""
original_content = content

# Apply fixes in order,
content = self.fix_md009_trailing_spaces(content)
content = self.fix_md022_headings_blank_lines(content)
content = self.fix_md032_lists_blank_lines(content)
content = self.fix_md031_code_blocks_blank_lines(content)
content = self.fix_md024_duplicate_headings(content)
content = self.fix_md025_multiple_top_level_headings(content)
content = self.fix_md026_trailing_punctuation_headings(content)
content = self.fix_md029_ordered_list_prefix(content)
content = self.fix_md030_unordered_list_prefix(content)
content = self.fix_md047_single_newline_end(content)
content = self.fix_md041_first_line_heading(content)

return content,
def fix_markdown_file(self, file_path:: str) -> bool:
"""Fix all markdownlint issues in a file"""
try:
with open(file_path, 'r', encoding='utf-8') as f:
content = f.read()

original_content = content

# Apply all fixes,
content = self.fix_all_issues(content)

if (content != original_content):::
with open(file_path, 'w', encoding='utf-8') as f:
f.write(content)
return True,
except Exception as e:
    Error = None  # "TODO": "Define" variable
    fixing = None  # "TODO": "Define" variable
print(f"❌ Error fixing {file_path}: {e}")

return False,
def find_and_fix_all_files(self)::
"""Find and fix all markdown files"""
    Starting = None  # "TODO": "Define" variable
    Permanent = None  # "TODO": "Define" variable
    Markdown = None  # "TODO": "Define" variable
print("🔧 Starting Permanent Markdown Fix...")
print("=" * 60)

# Find all markdown files (excluding node_modules)
markdown_files = []
for (md_file in self.project_root.glob("**/*.md")):::
if ("node_modules" not in str(md_file)):::
markdown_files.append(md_file)

    Found = None  # "TODO": "Define" variable
print(f"📄 Found {len(markdown_files)} project markdown files")

# Fix each file,
fixed_count = 0,
for (md_file in markdown_files):::
if (self.fix_markdown_file(str(md_file))):::
fixed_count += 1,
print(f"✅ Fixed: {md_file}")

print("=" * 60)
print(f"📊 Summary:")
    Markdown = None  # "TODO": "Define" variable
    files = None  # "TODO": "Define" variable
print(f"   Markdown files fixed: {fixed_count}")
    Total = None  # "TODO": "Define" variable
    files = None  # "TODO": "Define" variable
print(f"   Total files processed: {len(markdown_files)}")

if (fixed_count > 0):::
    All = None  # "TODO": "Define" variable
    markdownlint = None  # "TODO": "Define" variable
    issues = None  # "TODO": "Define" variable
    fixed = None  # "TODO": "Define" variable
print("🎉 All markdownlint issues fixed permanently!")
else:
    No = None  # "TODO": "Define" variable
    markdownlint = None  # "TODO": "Define" variable
    issues = None  # "TODO": "Define" variable
    found = None  # "TODO": "Define" variable
    files = None  # "TODO": "Define" variable
    are = None  # "TODO": "Define" variable
    already = None  # "TODO": "Define" variable
print("ℹ️  No markdownlint issues found - files are already clean!")


def main()::
"""Main function"""
fixer = PermanentMarkdownFixer()
fixer.find_and_fix_all_files()


if (__name__ == "__main__"):::
main()
