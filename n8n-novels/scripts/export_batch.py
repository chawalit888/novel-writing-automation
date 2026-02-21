#!/usr/bin/env python3
"""
Export Batch Script
Export หลายเรื่องพร้อมกัน
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
import argparse
import subprocess


class BatchExporter:
    """Export multiple novels at once"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.stories_path = self.base_path / "stories"
        self.exports_path = self.base_path / "outputs" / "exports"
        self.exports_path.mkdir(parents=True, exist_ok=True)

    def get_all_projects(self) -> List[Dict]:
        """Get all available projects"""
        projects = []

        if not self.stories_path.exists():
            return projects

        for project_dir in self.stories_path.iterdir():
            if not project_dir.is_dir():
                continue

            config_file = project_dir / "config.json"
            if not config_file.exists():
                continue

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Count chapters
            chapters_dir = project_dir / "chapters"
            chapter_count = len(list(chapters_dir.glob("*.txt"))) if chapters_dir.exists() else 0

            projects.append({
                "project_id": config.get("project_id", project_dir.name),
                "title": config.get("title", "Unknown"),
                "path": str(project_dir),
                "chapters": chapter_count,
                "target_chapters": config.get("target_chapters", 20)
            })

        return projects

    def merge_chapters(self, project_path: Path, start: int = 1, end: int = 999) -> str:
        """Merge chapters into single text"""
        chapters_dir = project_path / "chapters"
        content_parts = []

        # Get sorted chapter files
        chapter_files = sorted(chapters_dir.glob("ch-*.txt"))

        for ch_file in chapter_files:
            try:
                ch_num = int(ch_file.stem.split("-")[1])
                if start <= ch_num <= end:
                    with open(ch_file, 'r', encoding='utf-8') as f:
                        ch_content = f.read()
                    content_parts.append(f"# บทที่ {ch_num}\n\n{ch_content}")
            except (ValueError, IndexError):
                continue

        return "\n\n---\n\n".join(content_parts)

    def export_txt(self, project_id: str, output_name: str = None) -> Optional[Path]:
        """Export project to TXT"""
        project_path = self.stories_path / project_id

        if not project_path.exists():
            print(f"Project not found: {project_id}")
            return None

        # Load config
        config_file = project_path / "config.json"
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        title = config.get("title", project_id)
        content = self.merge_chapters(project_path)

        if not content:
            print(f"No chapters found for: {project_id}")
            return None

        # Create header
        header = f"""# {title}
โดย AI Writer

วันที่ export: {datetime.now().strftime("%Y-%m-%d")}

{'='*50}

"""
        full_content = header + content

        # Output path
        if output_name is None:
            output_name = project_id

        txt_dir = self.exports_path / "txt"
        txt_dir.mkdir(exist_ok=True)
        output_file = txt_dir / f"{output_name}.txt"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)

        return output_file

    def export_epub(self, project_id: str, output_name: str = None) -> Optional[Path]:
        """Export project to EPUB using pandoc"""
        project_path = self.stories_path / project_id

        if not project_path.exists():
            return None

        # First create markdown
        config_file = project_path / "config.json"
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        title = config.get("title", project_id)
        content = self.merge_chapters(project_path)

        if not content:
            return None

        # Create temp markdown
        md_content = f"""---
title: "{title}"
author: "AI Writer"
lang: th
---

{content}
"""
        temp_md = self.exports_path / "temp.md"
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(md_content)

        # Output path
        if output_name is None:
            output_name = project_id

        epub_dir = self.exports_path / "epub"
        epub_dir.mkdir(exist_ok=True)
        output_file = epub_dir / f"{output_name}.epub"

        try:
            cmd = [
                "pandoc", str(temp_md),
                "-o", str(output_file),
                "--toc"
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            temp_md.unlink()
            return output_file
        except Exception as e:
            print(f"EPUB export failed: {e}")
            return None

    def export_all(self, formats: List[str] = ["txt"],
                   min_chapters: int = 1) -> Dict[str, List[Path]]:
        """
        Export all projects that meet criteria

        Args:
            formats: Export formats (txt, epub)
            min_chapters: Minimum chapters required to export

        Returns:
            Dictionary of format -> list of exported files
        """
        projects = self.get_all_projects()
        results = {fmt: [] for fmt in formats}

        print(f"\n{'='*60}")
        print(f" BATCH EXPORT")
        print(f"{'='*60}")
        print(f" Formats: {', '.join(formats)}")
        print(f" Min chapters: {min_chapters}")
        print(f"{'='*60}\n")

        for project in projects:
            if project['chapters'] < min_chapters:
                print(f"⏭️  Skipping {project['title']} ({project['chapters']} chapters)")
                continue

            print(f"📖 Exporting: {project['title']}")

            for fmt in formats:
                if fmt == "txt":
                    result = self.export_txt(project['project_id'])
                elif fmt == "epub":
                    result = self.export_epub(project['project_id'])
                else:
                    continue

                if result:
                    results[fmt].append(result)
                    print(f"   ✅ {fmt.upper()}: {result.name}")

        # Summary
        print(f"\n{'='*60}")
        print(" EXPORT SUMMARY")
        print(f"{'='*60}")
        for fmt, files in results.items():
            print(f" {fmt.upper()}: {len(files)} files")
        print(f"{'='*60}\n")

        return results

    def export_weekly(self) -> Dict[str, List[Path]]:
        """Export this week's chapters"""
        week_dir = self.exports_path / "weekly" / datetime.now().strftime("week-%W")
        week_dir.mkdir(parents=True, exist_ok=True)

        # Get chapters written this week
        # (In production, check actual dates)

        results = self.export_all(formats=["txt", "epub"])

        # Copy to weekly folder
        for fmt, files in results.items():
            fmt_week_dir = week_dir / fmt
            fmt_week_dir.mkdir(exist_ok=True)
            for f in files:
                shutil.copy(f, fmt_week_dir)

        return results


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Batch export novels')
    parser.add_argument('--base-path', default=str(Path(__file__).parent.parent),
                        help='Base path for n8n-novels')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # List projects
    subparsers.add_parser('list', help='List available projects')

    # Export all
    all_parser = subparsers.add_parser('all', help='Export all projects')
    all_parser.add_argument('--format', nargs='+', default=['txt'],
                            choices=['txt', 'epub'], help='Export formats')
    all_parser.add_argument('--min-chapters', type=int, default=1,
                            help='Minimum chapters required')

    # Export single
    single_parser = subparsers.add_parser('single', help='Export single project')
    single_parser.add_argument('project_id', help='Project ID to export')
    single_parser.add_argument('--format', nargs='+', default=['txt'],
                               choices=['txt', 'epub'], help='Export formats')

    # Weekly export
    subparsers.add_parser('weekly', help='Export weekly compilation')

    args = parser.parse_args()

    exporter = BatchExporter(args.base_path)

    if args.command == 'list':
        projects = exporter.get_all_projects()
        if not projects:
            print("No projects found.")
        else:
            print(f"\n{'='*60}")
            print(f" Available Projects ({len(projects)})")
            print(f"{'='*60}")
            for p in projects:
                status = "✅" if p['chapters'] >= p['target_chapters'] else "📝"
                print(f" {status} {p['title']}")
                print(f"    ID: {p['project_id']}")
                print(f"    Chapters: {p['chapters']}/{p['target_chapters']}")
            print()

    elif args.command == 'all':
        exporter.export_all(
            formats=args.format,
            min_chapters=args.min_chapters
        )

    elif args.command == 'single':
        for fmt in args.format:
            if fmt == 'txt':
                result = exporter.export_txt(args.project_id)
            elif fmt == 'epub':
                result = exporter.export_epub(args.project_id)

            if result:
                print(f"✅ Exported: {result}")
            else:
                print(f"❌ Failed to export {fmt}")

    elif args.command == 'weekly':
        exporter.export_weekly()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
