import os
from pathlib import Path

#!/usr/bin/env python3
"""
EHB Markdown Issues Fixer
Automatically fixes all markdown linting issues
"""



class MarkdownFixer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.fixed_files = []
        self.issues_fixed = {
            "MD022": 0,  # Headings should be surrounded by blank lines
            "MD032": 0,  # Lists should be surrounded by blank lines
            "MD009": 0,  # No trailing spaces
            "MD047": 0,  # No trailing spaces
            "MD040": 0,  # Fenced code blocks should have language
            "MD031": 0,  # Fenced code blocks should be surrounded by blank lines
        }

    def fix_all_markdown_files(self):
        """Fix all markdown files in the project"""
        print("TOOLS Fixing markdown issues...")

        # Find all markdown files
        markdown_files = []
        for pattern in ["**/*.md", "**/*.markdown"]:
            markdown_files.extend(glob.glob(pattern, recursive=True))

        print(f"Found {len(markdown_files)} markdown files")

        for file_path in markdown_files:
            if self._should_fix_file(file_path):
                self._fix_markdown_file(file_path)

        self._print_summary()

    def _should_fix_file(self, file_path: str) -> bool:
        """Check if file should be fixed"""
        # Skip node_modules and other directories
        skip_patterns = ["node_modules", ".git", "dist", "build", "temp"]
        for pattern in skip_patterns:
            if pattern in file_path:
                return False
        return True

    def _fix_markdown_file(self, file_path: str):
        """Fix a single markdown file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Fix all issues
            content = self._fix_heading_blanks(content)
            content = self._fix_list_blanks(content)
            content = self._fix_trailing_spaces(content)
            content = self._fix_code_block_language(content)
            content = self._fix_code_block_blanks(content)

            # Only write if content changed
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                self.fixed_files.append(file_path)
                print(f"SUCCESS Fixed: {file_path}")

        except Exception as e:
            print(f"ERROR Error fixing {file_path}: {e}")

    def _fix_heading_blanks(self, content: str) -> str:
        """Fix MD022: Headings should be surrounded by blank lines"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Check if line is a heading
            if re.match(r"^#{1,6}\s+", line):
                # Add blank line before heading (except at start)
                if i > 0 and lines[i - 1].strip() != "":
                    fixed_lines.append("")

                fixed_lines.append(line)

                # Add blank line after heading (except at end)
                if i < len(lines) - 1 and lines[i + 1].strip() != "":
                    fixed_lines.append("")

                self.issues_fixed["MD022"] += 1
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _fix_list_blanks(self, content: str) -> str:
        """Fix MD032: Lists should be surrounded by blank lines"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Check if line is a list item
            if re.match(r"^[\s]*[-*+]\s+", line) or re.match(r"^[\s]*\d+\.\s+", line):
                # Add blank line before list (except at start)
                if (
                    i > 0
                    and lines[i - 1].strip() != ""
                    and not re.match(r"^[\s]*[-*+]\s+", lines[i - 1])
                    and not re.match(r"^[\s]*\d+\.\s+", lines[i - 1])
                ):
                    fixed_lines.append("")

                fixed_lines.append(line)

                # Add blank line after list (except at end)
                if (
                    i < len(lines) - 1
                    and lines[i + 1].strip() != ""
                    and not re.match(r"^[\s]*[-*+]\s+", lines[i + 1])
                    and not re.match(r"^[\s]*\d+\.\s+", lines[i + 1])
                ):
                    fixed_lines.append("")

                self.issues_fixed["MD032"] += 1
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _fix_trailing_spaces(self, content: str) -> str:
        """Fix MD009 and MD047: No trailing spaces"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Remove trailing spaces
            fixed_line = line.rstrip()
            if fixed_line != line:
                self.issues_fixed["MD009"] += 1
                self.issues_fixed["MD047"] += 1
            fixed_lines.append(fixed_line)

        return "\n".join(fixed_lines)

    def _fix_code_block_language(self, content: str) -> str:
        """Fix MD040: Fenced code blocks should have language"""
        # Find code blocks without language
        pattern = r"```\s*\n"
        replacement = r"```text\n"

        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            self.issues_fixed["MD040"] += matches

        return content

    def _fix_code_block_blanks(self, content: str) -> str:
        """Fix MD031: Fenced code blocks should be surrounded by blank lines"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Check if line is a code block fence
            if line.strip().startswith("```"):
                # Add blank line before code block (except at start)
                if i > 0 and lines[i - 1].strip() != "":
                    fixed_lines.append("")

                fixed_lines.append(line)

                # Add blank line after code block (except at end)
                if i < len(lines) - 1 and lines[i + 1].strip() != "":
                    fixed_lines.append("")

                self.issues_fixed["MD031"] += 1
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _print_summary(self):
        """Print summary of fixes"""
        print("\n" + "=" * 50)
        print("REPORT MARKDOWN FIXES SUMMARY")
        print("=" * 50)

        print(f"SUCCESS Files fixed: {len(self.fixed_files)}")
        print("\nIssues fixed:")
        for issue, count in self.issues_fixed.items():
            if count > 0:
                print(f"  - {issue}: {count} fixes")

        if self.fixed_files:
            print(f"\nFixed files:")
            for file_path in self.fixed_files:
                print(f"  - {file_path}")

        print("\n🎉 All markdown issues have been fixed!")
        print("=" * 50)


def main():
    """Main function"""
    fixer = MarkdownFixer()
    fixer.fix_all_markdown_files()


if __name__ == "__main__":
    main()
