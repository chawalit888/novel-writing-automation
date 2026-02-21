#!/usr/bin/env python3
"""
Stats Tracker Tool
ติดตามสถิติการเขียนนิยาย
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class ChapterStats:
    """Statistics for a single chapter"""
    chapter_num: int
    word_count: int
    character_count: int
    paragraph_count: int
    dialogue_percentage: float
    created_date: str
    modified_date: str


@dataclass
class ProjectStats:
    """Statistics for entire project"""
    project_name: str
    total_chapters: int
    total_words: int
    average_words_per_chapter: float
    total_characters_used: int
    unique_characters: int
    completion_percentage: float
    estimated_completion_date: Optional[str]
    chapters: List[ChapterStats]
    words_per_day: Dict[str, int]
    genre: str = ""
    target_chapters: int = 25


class StatsTracker:
    """Track and analyze project statistics"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.stats_file = self.project_path / "metadata" / "stats.json"

    def count_words(self, text: str) -> int:
        """Count words in text (Thai-aware)"""
        # Simple word count - for Thai, might need more sophisticated method
        # This counts spaces and newlines as word separators
        return len(text.split())

    def count_dialogues(self, text: str) -> float:
        """Calculate percentage of dialogue in text"""
        import re
        dialogue_pattern = r'"[^"]*"|"[^"]*"'
        dialogues = re.findall(dialogue_pattern, text)
        dialogue_chars = sum(len(d) for d in dialogues)
        total_chars = len(text)
        return (dialogue_chars / total_chars * 100) if total_chars > 0 else 0

    def analyze_chapter(self, chapter_num: int) -> Optional[ChapterStats]:
        """Analyze a single chapter"""
        chapter_path = self.project_path / "chapters" / f"chapter-{chapter_num:03d}.txt"

        if not chapter_path.exists():
            return None

        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()

        stat = os.stat(chapter_path)

        return ChapterStats(
            chapter_num=chapter_num,
            word_count=self.count_words(content),
            character_count=len(content),
            paragraph_count=len([p for p in content.split('\n\n') if p.strip()]),
            dialogue_percentage=round(self.count_dialogues(content), 2),
            created_date=datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d"),
            modified_date=datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
        )

    def get_characters_used(self) -> tuple:
        """Get character usage statistics"""
        chars_path = self.project_path / "characters"
        if not chars_path.exists():
            return 0, 0

        total = 0
        unique = set()

        for char_file in chars_path.glob("*.json"):
            total += 1
            with open(char_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                unique.add(data.get('name', char_file.stem))

        return total, len(unique)

    def calculate_writing_pace(self, chapter_stats: List[ChapterStats]) -> Dict[str, int]:
        """Calculate words written per day"""
        words_per_day = defaultdict(int)

        for ch in chapter_stats:
            words_per_day[ch.created_date] += ch.word_count

        return dict(words_per_day)

    def estimate_completion(self, chapter_stats: List[ChapterStats], target_chapters: int) -> Optional[str]:
        """Estimate completion date based on writing pace"""
        if len(chapter_stats) < 2:
            return None

        # Calculate average days per chapter
        dates = sorted(set(ch.created_date for ch in chapter_stats))
        if len(dates) < 2:
            return None

        first_date = datetime.strptime(dates[0], "%Y-%m-%d")
        last_date = datetime.strptime(dates[-1], "%Y-%m-%d")
        days_elapsed = (last_date - first_date).days

        if days_elapsed == 0:
            return None

        chapters_completed = len(chapter_stats)
        chapters_per_day = chapters_completed / days_elapsed

        if chapters_per_day == 0:
            return None

        chapters_remaining = target_chapters - chapters_completed
        days_remaining = int(chapters_remaining / chapters_per_day)

        estimated_date = datetime.now() + timedelta(days=days_remaining)
        return estimated_date.strftime("%Y-%m-%d")

    def load_project_config(self) -> Dict:
        """Load project configuration"""
        config_path = self.project_path / "PROJECT.md"
        config = {"genre": "", "target_chapters": 25}

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple parsing - in production use proper parser
                if "Genre:" in content:
                    for line in content.split('\n'):
                        if "Genre:" in line:
                            config["genre"] = line.split(":")[-1].strip()
                        if "Target Chapters:" in line:
                            try:
                                config["target_chapters"] = int(line.split(":")[-1].strip())
                            except ValueError:
                                pass

        return config

    def analyze_project(self) -> ProjectStats:
        """Analyze entire project"""
        config = self.load_project_config()
        target_chapters = config.get("target_chapters", 25)

        # Analyze all chapters
        chapter_stats = []
        for i in range(1, 200):  # Assume max 200 chapters
            stats = self.analyze_chapter(i)
            if stats:
                chapter_stats.append(stats)

        total_words = sum(ch.word_count for ch in chapter_stats)
        total_chars, unique_chars = self.get_characters_used()

        project_stats = ProjectStats(
            project_name=self.project_path.name,
            total_chapters=len(chapter_stats),
            total_words=total_words,
            average_words_per_chapter=round(total_words / len(chapter_stats), 2) if chapter_stats else 0,
            total_characters_used=total_chars,
            unique_characters=unique_chars,
            completion_percentage=round(len(chapter_stats) / target_chapters * 100, 2) if target_chapters else 0,
            estimated_completion_date=self.estimate_completion(chapter_stats, target_chapters),
            chapters=chapter_stats,
            words_per_day=self.calculate_writing_pace(chapter_stats),
            genre=config.get("genre", ""),
            target_chapters=target_chapters
        )

        return project_stats

    def save_stats(self, stats: ProjectStats):
        """Save stats to JSON file"""
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict, handling nested dataclasses
        stats_dict = asdict(stats)

        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, ensure_ascii=False, indent=2)

        print(f"Stats saved to: {self.stats_file}")

    def print_summary(self, stats: ProjectStats):
        """Print formatted summary"""
        print("\n" + "=" * 60)
        print(f" PROJECT STATS: {stats.project_name}")
        print("=" * 60)
        print(f" Genre:              {stats.genre}")
        print(f" Total Chapters:     {stats.total_chapters}/{stats.target_chapters}")
        print(f" Completion:         {stats.completion_percentage}%")
        print(f" Total Words:        {stats.total_words:,}")
        print(f" Avg Words/Chapter:  {stats.average_words_per_chapter:,.0f}")
        print(f" Characters Used:    {stats.unique_characters}")

        if stats.estimated_completion_date:
            print(f" Est. Completion:    {stats.estimated_completion_date}")

        print("-" * 60)
        print(" RECENT CHAPTERS:")
        for ch in stats.chapters[-5:]:
            print(f"   Chapter {ch.chapter_num}: {ch.word_count:,} words ({ch.created_date})")

        print("=" * 60 + "\n")


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Track project statistics')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--save', action='store_true', help='Save stats to file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    tracker = StatsTracker(args.project_path)
    stats = tracker.analyze_project()

    if args.json:
        print(json.dumps(asdict(stats), ensure_ascii=False, indent=2))
    else:
        tracker.print_summary(stats)

    if args.save:
        tracker.save_stats(stats)


if __name__ == "__main__":
    main()
