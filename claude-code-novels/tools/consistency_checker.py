#!/usr/bin/env python3
"""
Consistency Checker Tool
ตรวจสอบความสอดคล้องของนิยาย: ตัวละคร, timeline, world building
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


@dataclass
class Issue:
    """Represents a consistency issue found"""
    severity: Severity
    category: str
    description: str
    location: str
    suggestion: str = ""


@dataclass
class ConsistencyReport:
    """Report containing all found issues"""
    project_name: str
    chapters_reviewed: str
    date: str
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue):
        self.issues.append(issue)

    def get_by_severity(self, severity: Severity) -> List[Issue]:
        return [i for i in self.issues if i.severity == severity]

    def to_markdown(self) -> str:
        """Generate markdown report"""
        lines = [
            f"# Consistency Report: {self.project_name}",
            f"## Chapters Reviewed: {self.chapters_reviewed}",
            f"## Date: {self.date}",
            "",
            "---",
            ""
        ]

        # Critical Issues
        critical = self.get_by_severity(Severity.CRITICAL)
        lines.append("## Critical Issues (ต้องแก้ไขทันที)")
        if critical:
            for i, issue in enumerate(critical, 1):
                lines.extend([
                    f"\n### Issue #{i}",
                    f"- **Category:** {issue.category}",
                    f"- **Location:** {issue.location}",
                    f"- **Description:** {issue.description}",
                    f"- **Suggestion:** {issue.suggestion}",
                ])
        else:
            lines.append("\nNo critical issues found.")

        # Major Issues
        lines.append("\n---\n")
        lines.append("## Major Issues (ควรแก้ไข)")
        major = self.get_by_severity(Severity.MAJOR)
        if major:
            for i, issue in enumerate(major, 1):
                lines.extend([
                    f"\n### Issue #{i}",
                    f"- **Category:** {issue.category}",
                    f"- **Location:** {issue.location}",
                    f"- **Description:** {issue.description}",
                    f"- **Suggestion:** {issue.suggestion}",
                ])
        else:
            lines.append("\nNo major issues found.")

        # Minor Issues
        lines.append("\n---\n")
        lines.append("## Minor Issues (แก้ไขถ้ามีเวลา)")
        minor = self.get_by_severity(Severity.MINOR)
        if minor:
            for i, issue in enumerate(minor, 1):
                lines.extend([
                    f"\n### Issue #{i}",
                    f"- **Category:** {issue.category}",
                    f"- **Location:** {issue.location}",
                    f"- **Description:** {issue.description}",
                ])
        else:
            lines.append("\nNo minor issues found.")

        # Summary
        lines.extend([
            "\n---\n",
            "## Summary",
            f"- Critical: {len(critical)}",
            f"- Major: {len(major)}",
            f"- Minor: {len(minor)}",
            f"- **Total: {len(self.issues)}**",
        ])

        return "\n".join(lines)


class ConsistencyChecker:
    """Main consistency checker class"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.characters: Dict = {}
        self.world_rules: Dict = {}
        self.timeline: List = []
        self.report: Optional[ConsistencyReport] = None

    def load_project_data(self):
        """Load all project data"""
        # Load characters
        char_path = self.project_path / "characters"
        if char_path.exists():
            for char_file in char_path.glob("*.json"):
                with open(char_file, 'r', encoding='utf-8') as f:
                    char_data = json.load(f)
                    self.characters[char_data.get('name', char_file.stem)] = char_data

        # Load world rules
        world_path = self.project_path / "world"
        if world_path.exists():
            for world_file in world_path.glob("*.md"):
                with open(world_file, 'r', encoding='utf-8') as f:
                    self.world_rules[world_file.stem] = f.read()

        # Load timeline
        timeline_path = self.project_path / "metadata" / "timeline.json"
        if timeline_path.exists():
            with open(timeline_path, 'r', encoding='utf-8') as f:
                self.timeline = json.load(f)

    def check_chapter(self, chapter_num: int) -> List[Issue]:
        """Check a single chapter for issues"""
        issues = []
        chapter_path = self.project_path / "chapters" / f"chapter-{chapter_num:03d}.txt"

        if not chapter_path.exists():
            return issues

        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check character name consistency
        issues.extend(self._check_character_names(content, chapter_num))

        # Check for common issues
        issues.extend(self._check_common_issues(content, chapter_num))

        return issues

    def _check_character_names(self, content: str, chapter_num: int) -> List[Issue]:
        """Check for character name misspellings"""
        issues = []

        for char_name in self.characters.keys():
            # Look for potential misspellings (simple check)
            # In production, use fuzzy matching
            pattern = re.compile(re.escape(char_name), re.IGNORECASE)
            matches = pattern.findall(content)

            # Check if name appears with different capitalizations
            if len(set(matches)) > 1:
                issues.append(Issue(
                    severity=Severity.MINOR,
                    category="Character",
                    description=f"Character name '{char_name}' appears with inconsistent capitalization",
                    location=f"Chapter {chapter_num}",
                    suggestion="Standardize the character name throughout"
                ))

        return issues

    def _check_common_issues(self, content: str, chapter_num: int) -> List[Issue]:
        """Check for common writing issues"""
        issues = []

        # Check for placeholder text
        placeholders = re.findall(r'\[.*?\]|\{.*?\}|TODO|FIXME|XXX', content)
        if placeholders:
            issues.append(Issue(
                severity=Severity.CRITICAL,
                category="Content",
                description=f"Found placeholder text: {placeholders[:3]}",
                location=f"Chapter {chapter_num}",
                suggestion="Replace or remove placeholder text"
            ))

        # Check for repeated phrases
        words = content.split()
        word_count = len(words)

        if word_count < 2000:
            issues.append(Issue(
                severity=Severity.MAJOR,
                category="Length",
                description=f"Chapter too short ({word_count} words)",
                location=f"Chapter {chapter_num}",
                suggestion="Expand the chapter to at least 3000 words"
            ))
        elif word_count > 8000:
            issues.append(Issue(
                severity=Severity.MINOR,
                category="Length",
                description=f"Chapter very long ({word_count} words)",
                location=f"Chapter {chapter_num}",
                suggestion="Consider splitting into multiple chapters"
            ))

        return issues

    def run_check(self, start_chapter: int = 1, end_chapter: int = 100) -> ConsistencyReport:
        """Run consistency check on range of chapters"""
        self.load_project_data()

        project_name = self.project_path.name
        self.report = ConsistencyReport(
            project_name=project_name,
            chapters_reviewed=f"{start_chapter}-{end_chapter}",
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        for chapter_num in range(start_chapter, end_chapter + 1):
            chapter_issues = self.check_chapter(chapter_num)
            for issue in chapter_issues:
                self.report.add_issue(issue)

        return self.report

    def save_report(self, output_path: Optional[str] = None):
        """Save report to file"""
        if not self.report:
            raise ValueError("No report to save. Run check first.")

        if output_path is None:
            output_path = self.project_path / "metadata" / "consistency_report.md"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.report.to_markdown())

        print(f"Report saved to: {output_path}")
        return output_path


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Check novel consistency')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--start', type=int, default=1, help='Start chapter')
    parser.add_argument('--end', type=int, default=100, help='End chapter')
    parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    checker = ConsistencyChecker(args.project_path)
    report = checker.run_check(args.start, args.end)

    print(report.to_markdown())

    if args.output:
        checker.save_report(args.output)


if __name__ == "__main__":
    main()
