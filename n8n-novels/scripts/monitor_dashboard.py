#!/usr/bin/env python3
"""
Monitor Dashboard for n8n Novel System
แสดงสถานะการทำงานของระบบ
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse


class NovelDashboard:
    """Dashboard for monitoring novel writing system"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.stories_path = self.base_path / "stories"
        self.logs_path = self.base_path / "logs"

    def get_all_projects(self) -> List[Dict]:
        """Get all projects with their status"""
        projects = []

        if not self.stories_path.exists():
            return projects

        for project_dir in self.stories_path.iterdir():
            if not project_dir.is_dir():
                continue

            config_file = project_dir / "config.json"
            metadata_file = project_dir / "metadata.json"

            if not config_file.exists():
                continue

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            metadata = {}
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

            # Count chapters
            chapters_dir = project_dir / "chapters"
            chapter_count = len(list(chapters_dir.glob("*.txt"))) if chapters_dir.exists() else 0

            # Count words
            total_words = 0
            if chapters_dir.exists():
                for ch_file in chapters_dir.glob("*.txt"):
                    with open(ch_file, 'r', encoding='utf-8') as f:
                        total_words += len(f.read().split())

            projects.append({
                "project_id": config.get("project_id", project_dir.name),
                "title": config.get("title", "Unknown"),
                "genre": config.get("genre", "Unknown"),
                "ai_model": config.get("ai_model", "Unknown"),
                "target_chapters": config.get("target_chapters", 20),
                "current_chapters": chapter_count,
                "total_words": total_words,
                "status": metadata.get("status", "unknown"),
                "last_activity": metadata.get("last_activity"),
                "completion": round(chapter_count / config.get("target_chapters", 20) * 100, 1)
            })

        return projects

    def get_today_stats(self) -> Dict:
        """Get statistics for today"""
        today = datetime.now().strftime("%Y-%m-%d")

        stats = {
            "chapters_written": 0,
            "words_written": 0,
            "workflows_run": 0,
            "errors": 0,
            "api_cost_usd": 0
        }

        # Check daily output directory
        daily_output = self.base_path / "outputs" / "daily" / today
        if daily_output.exists():
            for ch_file in daily_output.glob("*.txt"):
                stats["chapters_written"] += 1
                with open(ch_file, 'r', encoding='utf-8') as f:
                    stats["words_written"] += len(f.read().split())

        # Check execution logs
        exec_log = self.logs_path / "execution-logs" / f"{today}.json"
        if exec_log.exists():
            with open(exec_log, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                stats["workflows_run"] = len(logs)
                stats["errors"] = sum(1 for l in logs if l.get("status") == "failed")
                stats["api_cost_usd"] = sum(l.get("api_cost_usd", 0) for l in logs)

        return stats

    def get_recent_errors(self, limit: int = 5) -> List[Dict]:
        """Get recent errors from logs"""
        errors = []
        error_log_dir = self.logs_path / "error-logs"

        if not error_log_dir.exists():
            return errors

        error_files = sorted(error_log_dir.glob("*.json"), reverse=True)[:limit]

        for error_file in error_files:
            with open(error_file, 'r', encoding='utf-8') as f:
                error_data = json.load(f)
                errors.append({
                    "date": error_file.stem,
                    "workflow": error_data.get("workflow", "Unknown"),
                    "error": error_data.get("error_message", "No message")[:100]
                })

        return errors

    def get_quality_stats(self) -> Dict:
        """Get quality statistics from QC reports"""
        qc_dir = self.logs_path / "qc-reports"

        stats = {
            "total_reviewed": 0,
            "approved": 0,
            "flagged": 0,
            "regenerated": 0,
            "average_score": 0
        }

        if not qc_dir.exists():
            return stats

        scores = []
        for qc_file in qc_dir.glob("*.json"):
            with open(qc_file, 'r', encoding='utf-8') as f:
                qc_data = json.load(f)
                stats["total_reviewed"] += 1
                scores.append(qc_data.get("overall_score", 0))

                verdict = qc_data.get("verdict", "").lower()
                if verdict == "approve":
                    stats["approved"] += 1
                elif verdict == "flag":
                    stats["flagged"] += 1
                elif verdict == "regenerate":
                    stats["regenerated"] += 1

        if scores:
            stats["average_score"] = round(sum(scores) / len(scores), 1)

        return stats

    def print_dashboard(self):
        """Print formatted dashboard"""
        projects = self.get_all_projects()
        today_stats = self.get_today_stats()
        quality_stats = self.get_quality_stats()
        recent_errors = self.get_recent_errors(3)

        # Header
        print("\n" + "=" * 70)
        print(" 📊 N8N NOVEL WRITING SYSTEM - DASHBOARD".center(70))
        print("=" * 70)
        print(f" 📅 {datetime.now().strftime('%A, %B %d, %Y - %H:%M:%S')}".center(70))
        print("=" * 70)

        # Today's Stats
        print("\n🎯 TODAY'S ACTIVITY")
        print("-" * 70)
        print(f" Chapters Written:  {today_stats['chapters_written']}")
        print(f" Words Written:     {today_stats['words_written']:,}")
        print(f" Workflows Run:     {today_stats['workflows_run']}")
        print(f" Errors:            {today_stats['errors']}")
        print(f" API Cost:          ${today_stats['api_cost_usd']:.2f}")

        # Quality Stats
        print("\n📈 QUALITY METRICS")
        print("-" * 70)
        print(f" Total Reviewed:    {quality_stats['total_reviewed']}")
        print(f" Auto-Approved:     {quality_stats['approved']}")
        print(f" Flagged:           {quality_stats['flagged']}")
        print(f" Regenerated:       {quality_stats['regenerated']}")
        print(f" Average Score:     {quality_stats['average_score']}/100")

        # Projects
        print("\n📚 ACTIVE PROJECTS")
        print("-" * 70)

        if not projects:
            print(" No projects found.")
        else:
            # Sort by completion
            projects.sort(key=lambda x: x['completion'], reverse=True)

            for p in projects[:10]:  # Show top 10
                progress_bar = self._make_progress_bar(p['completion'])
                print(f" {p['title'][:25]:<25} | {p['genre']:<15} | {progress_bar} {p['completion']}%")
                print(f"   Chapters: {p['current_chapters']}/{p['target_chapters']} | Words: {p['total_words']:,} | Model: {p['ai_model']}")

        # Recent Errors
        if recent_errors:
            print("\n⚠️  RECENT ERRORS")
            print("-" * 70)
            for err in recent_errors:
                print(f" [{err['date']}] {err['workflow']}: {err['error'][:50]}...")

        # Footer
        print("\n" + "=" * 70)
        print(" Use 'docker logs n8n-novels' for detailed workflow logs".center(70))
        print("=" * 70 + "\n")

    def _make_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Create ASCII progress bar"""
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"

    def export_json(self) -> Dict:
        """Export all stats as JSON"""
        return {
            "timestamp": datetime.now().isoformat(),
            "projects": self.get_all_projects(),
            "today": self.get_today_stats(),
            "quality": self.get_quality_stats(),
            "recent_errors": self.get_recent_errors()
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Novel system monitoring dashboard')
    parser.add_argument('--base-path', default=str(Path(__file__).parent.parent),
                        help='Base path for n8n-novels')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--watch', action='store_true',
                        help='Watch mode (refresh every 60s)')

    args = parser.parse_args()

    dashboard = NovelDashboard(args.base_path)

    if args.json:
        print(json.dumps(dashboard.export_json(), ensure_ascii=False, indent=2))
    elif args.watch:
        import time
        try:
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                dashboard.print_dashboard()
                print("\n[Press Ctrl+C to exit. Refreshing in 60 seconds...]")
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        dashboard.print_dashboard()


if __name__ == "__main__":
    main()
