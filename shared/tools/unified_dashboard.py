#!/usr/bin/env python3
"""
Unified Dashboard
แสดงสถานะทั้ง 2 ระบบในที่เดียว (Claude Code + n8n)
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class UnifiedDashboard:
    """Combined dashboard for both novel writing systems"""

    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Auto-detect from script location
            self.base_dir = Path(__file__).parent.parent.parent

        self.claude_code_path = self.base_dir / "claude-code-novels"
        self.n8n_path = self.base_dir / "n8n-novels"

    def get_claude_code_stats(self) -> Dict:
        """Get statistics from Claude Code projects"""
        projects_dir = self.claude_code_path / "projects"

        stats = {
            "total_projects": 0,
            "total_chapters": 0,
            "total_words": 0,
            "projects": []
        }

        if not projects_dir.exists():
            return stats

        for project_path in projects_dir.iterdir():
            if not project_path.is_dir():
                continue

            stats["total_projects"] += 1
            project_stats = {
                "name": project_path.name,
                "chapters": 0,
                "words": 0
            }

            chapters_dir = project_path / "chapters"
            if chapters_dir.exists():
                for chapter_file in chapters_dir.glob("*.txt"):
                    project_stats["chapters"] += 1
                    try:
                        with open(chapter_file, 'r', encoding='utf-8') as f:
                            words = len(f.read().split())
                            project_stats["words"] += words
                    except Exception:
                        pass

            stats["total_chapters"] += project_stats["chapters"]
            stats["total_words"] += project_stats["words"]
            stats["projects"].append(project_stats)

        return stats

    def get_n8n_stats(self) -> Dict:
        """Get statistics from n8n projects"""
        stories_dir = self.n8n_path / "stories"

        stats = {
            "total_projects": 0,
            "total_chapters": 0,
            "total_words": 0,
            "avg_quality_today": 0,
            "chapters_today": 0,
            "projects": []
        }

        if not stories_dir.exists():
            return stats

        for project_path in stories_dir.iterdir():
            if not project_path.is_dir():
                continue

            stats["total_projects"] += 1
            project_stats = {
                "name": project_path.name,
                "chapters": 0,
                "words": 0
            }

            # Check config for project name
            config_file = project_path / "config.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    project_stats["name"] = config.get("title", project_path.name)

            chapters_dir = project_path / "chapters"
            if chapters_dir.exists():
                for chapter_file in chapters_dir.glob("*.txt"):
                    project_stats["chapters"] += 1
                    try:
                        with open(chapter_file, 'r', encoding='utf-8') as f:
                            project_stats["words"] += len(f.read().split())
                    except Exception:
                        pass

            stats["total_chapters"] += project_stats["chapters"]
            stats["total_words"] += project_stats["words"]
            stats["projects"].append(project_stats)

        return stats

    def print_dashboard(self):
        """Print unified dashboard"""
        print("\n" + "=" * 70)
        print(" 📊 NOVEL WRITING EMPIRE - UNIFIED DASHBOARD".center(70))
        print("=" * 70)
        print(f" 📅 {datetime.now().strftime('%A, %B %d, %Y - %H:%M:%S')}".center(70))
        print("=" * 70)

        # Claude Code Stats
        print("\n🎯 CLAUDE CODE SYSTEM (Premium Quality)")
        print("-" * 70)
        claude_stats = self.get_claude_code_stats()
        print(f" Active Projects:  {claude_stats['total_projects']}")
        print(f" Total Chapters:   {claude_stats['total_chapters']}")
        print(f" Total Words:      {claude_stats['total_words']:,}")
        if claude_stats['total_chapters'] > 0:
            avg_words = claude_stats['total_words'] // claude_stats['total_chapters']
            print(f" Avg Words/Ch:     {avg_words:,}")

        if claude_stats['projects']:
            print("\n Projects:")
            for p in claude_stats['projects'][:5]:
                print(f"   • {p['name']}: {p['chapters']} chapters, {p['words']:,} words")

        # n8n Stats
        print("\n🤖 N8N MULTI-AI SYSTEM (High Volume)")
        print("-" * 70)
        n8n_stats = self.get_n8n_stats()
        print(f" Active Projects:  {n8n_stats['total_projects']}")
        print(f" Total Chapters:   {n8n_stats['total_chapters']}")
        print(f" Total Words:      {n8n_stats['total_words']:,}")

        if n8n_stats['projects']:
            print("\n Projects:")
            for p in n8n_stats['projects'][:5]:
                print(f"   • {p['name']}: {p['chapters']} chapters, {p['words']:,} words")

        # Combined Stats
        print("\n📈 COMBINED STATISTICS")
        print("-" * 70)
        total_projects = claude_stats['total_projects'] + n8n_stats['total_projects']
        total_chapters = claude_stats['total_chapters'] + n8n_stats['total_chapters']
        total_words = claude_stats['total_words'] + n8n_stats['total_words']

        print(f" Total Projects:   {total_projects}")
        print(f" Total Chapters:   {total_chapters}")
        print(f" Total Words:      {total_words:,}")
        if total_chapters > 0:
            print(f" Avg Words/Ch:     {total_words // total_chapters:,}")

        # Revenue Projection
        print("\n💰 REVENUE PROJECTION (if all sold)")
        print("-" * 70)
        claude_revenue = claude_stats['total_chapters'] * 150  # 150 THB avg
        n8n_revenue = n8n_stats['total_chapters'] * 40  # 40 THB avg
        total_revenue = claude_revenue + n8n_revenue

        print(f" Claude Code Est:  ฿{claude_revenue:,}")
        print(f" n8n Est:          ฿{n8n_revenue:,}")
        print(f" TOTAL POTENTIAL:  ฿{total_revenue:,}")

        # Progress Bar
        print("\n📊 MONTHLY TARGET PROGRESS")
        print("-" * 70)
        target_chapters_month = 300  # 10 chapters/day × 30 days
        progress = min((total_chapters / target_chapters_month) * 100, 100) if target_chapters_month > 0 else 0
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f" Monthly Target:   [{bar}] {progress:.1f}%")
        print(f" {total_chapters}/{target_chapters_month} chapters")

        print("\n" + "=" * 70 + "\n")

    def export_json(self) -> Dict:
        """Export stats as JSON"""
        return {
            "timestamp": datetime.now().isoformat(),
            "claude_code": self.get_claude_code_stats(),
            "n8n": self.get_n8n_stats()
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Unified novel writing dashboard')
    parser.add_argument('--base-dir', help='Base directory containing both systems')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--watch', action='store_true', help='Watch mode')

    args = parser.parse_args()

    dashboard = UnifiedDashboard(args.base_dir)

    if args.json:
        print(json.dumps(dashboard.export_json(), ensure_ascii=False, indent=2))
    elif args.watch:
        import time
        try:
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                dashboard.print_dashboard()
                print("[Press Ctrl+C to exit. Refreshing in 60s...]")
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        dashboard.print_dashboard()


if __name__ == "__main__":
    main()
