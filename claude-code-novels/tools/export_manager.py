#!/usr/bin/env python3
"""
Export Manager Tool
จัดการ export นิยายเป็น TXT, EPUB, PDF
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class ExportConfig:
    """Configuration for export"""
    title: str
    author: str
    chapters: List[int]
    output_format: str  # txt, epub, pdf
    output_path: str
    include_toc: bool = True
    chapter_break: str = "\n\n---\n\n"


class ExportManager:
    """Manage novel exports to various formats"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.chapters_path = self.project_path / "chapters"
        self.exports_path = self.project_path / "exports"
        self.exports_path.mkdir(parents=True, exist_ok=True)

    def load_project_info(self) -> Dict:
        """Load project information"""
        info = {
            "title": self.project_path.name,
            "author": "Anonymous",
            "description": ""
        }

        project_file = self.project_path / "PROJECT.md"
        if project_file.exists():
            with open(project_file, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.split('\n'):
                    if line.startswith("# "):
                        info["title"] = line[2:].strip()
                    elif "Author:" in line:
                        info["author"] = line.split(":")[-1].strip()
                    elif "Description:" in line:
                        info["description"] = line.split(":")[-1].strip()

        return info

    def get_chapter_content(self, chapter_num: int) -> Optional[str]:
        """Get content of a specific chapter"""
        chapter_file = self.chapters_path / f"chapter-{chapter_num:03d}.txt"
        if chapter_file.exists():
            with open(chapter_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def get_all_chapters(self) -> List[int]:
        """Get list of all available chapter numbers"""
        chapters = []
        if self.chapters_path.exists():
            for f in self.chapters_path.glob("chapter-*.txt"):
                try:
                    num = int(f.stem.split("-")[1])
                    chapters.append(num)
                except (IndexError, ValueError):
                    continue
        return sorted(chapters)

    def merge_chapters(self, chapter_nums: List[int], include_titles: bool = True) -> str:
        """Merge multiple chapters into single text"""
        parts = []

        for num in chapter_nums:
            content = self.get_chapter_content(num)
            if content:
                if include_titles:
                    parts.append(f"# บทที่ {num}\n\n{content}")
                else:
                    parts.append(content)

        return "\n\n---\n\n".join(parts)

    def export_txt(self, config: ExportConfig) -> Path:
        """Export to TXT format"""
        content = self.merge_chapters(config.chapters)

        # Add header
        header = f"""# {config.title}
โดย {config.author}

วันที่ export: {datetime.now().strftime("%Y-%m-%d")}
จำนวนบท: {len(config.chapters)}

{'='*50}

"""
        full_content = header + content

        output_file = self.exports_path / f"{config.output_path}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"Exported TXT to: {output_file}")
        return output_file

    def export_markdown(self, config: ExportConfig) -> Path:
        """Export to Markdown format (for EPUB/PDF conversion)"""
        content = self.merge_chapters(config.chapters)

        # Create markdown with metadata
        md_content = f"""---
title: "{config.title}"
author: "{config.author}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
lang: th
---

{content}
"""
        output_file = self.exports_path / f"{config.output_path}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return output_file

    def export_epub(self, config: ExportConfig) -> Optional[Path]:
        """Export to EPUB format using pandoc"""
        # First create markdown
        md_file = self.export_markdown(config)

        # Create EPUB directory
        epub_dir = self.exports_path / "epub"
        epub_dir.mkdir(exist_ok=True)

        output_file = epub_dir / f"{config.output_path}.epub"

        # Try to use pandoc
        try:
            cmd = [
                "pandoc",
                str(md_file),
                "-o", str(output_file),
                f"--metadata=title:{config.title}",
                f"--metadata=author:{config.author}",
                "--toc" if config.include_toc else "",
            ]
            cmd = [c for c in cmd if c]  # Remove empty strings

            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Exported EPUB to: {output_file}")
            return output_file

        except FileNotFoundError:
            print("Warning: pandoc not found. Please install pandoc for EPUB export.")
            print("Install with: brew install pandoc")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error creating EPUB: {e}")
            return None

    def export_pdf(self, config: ExportConfig) -> Optional[Path]:
        """Export to PDF format using pandoc"""
        # First create markdown
        md_file = self.export_markdown(config)

        # Create PDF directory
        pdf_dir = self.exports_path / "pdf"
        pdf_dir.mkdir(exist_ok=True)

        output_file = pdf_dir / f"{config.output_path}.pdf"

        # Try to use pandoc
        try:
            cmd = [
                "pandoc",
                str(md_file),
                "-o", str(output_file),
                f"--metadata=title:{config.title}",
                f"--metadata=author:{config.author}",
                "--pdf-engine=xelatex",  # Better Thai support
                "-V", "mainfont=TH Sarabun New",  # Thai font
                "--toc" if config.include_toc else "",
            ]
            cmd = [c for c in cmd if c]

            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Exported PDF to: {output_file}")
            return output_file

        except FileNotFoundError:
            print("Warning: pandoc not found. Please install pandoc for PDF export.")
            print("Install with: brew install pandoc")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error creating PDF: {e}")
            print("Note: PDF export requires LaTeX. Install with: brew install --cask mactex")
            return None

    def export(self, chapters: Optional[List[int]] = None,
               formats: List[str] = ["txt"],
               output_name: Optional[str] = None) -> Dict[str, Path]:
        """
        Export novel to specified formats

        Args:
            chapters: List of chapter numbers to export (None = all)
            formats: List of formats ("txt", "epub", "pdf")
            output_name: Base name for output files

        Returns:
            Dictionary of format -> output path
        """
        project_info = self.load_project_info()

        if chapters is None:
            chapters = self.get_all_chapters()

        if not chapters:
            print("No chapters found to export")
            return {}

        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{project_info['title']}_{timestamp}"

        # Clean filename
        output_name = "".join(c for c in output_name if c.isalnum() or c in "._- ")

        config = ExportConfig(
            title=project_info['title'],
            author=project_info['author'],
            chapters=chapters,
            output_format="",
            output_path=output_name
        )

        results = {}

        for fmt in formats:
            if fmt == "txt":
                results["txt"] = self.export_txt(config)
            elif fmt == "epub":
                result = self.export_epub(config)
                if result:
                    results["epub"] = result
            elif fmt == "pdf":
                result = self.export_pdf(config)
                if result:
                    results["pdf"] = result
            else:
                print(f"Unknown format: {fmt}")

        return results


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Export novel to various formats')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--chapters', nargs='+', type=int, help='Chapters to export')
    parser.add_argument('--format', nargs='+', default=['txt'],
                        choices=['txt', 'epub', 'pdf'], help='Export formats')
    parser.add_argument('--output', help='Output filename (without extension)')

    args = parser.parse_args()

    manager = ExportManager(args.project_path)
    results = manager.export(
        chapters=args.chapters,
        formats=args.format,
        output_name=args.output
    )

    print("\nExport complete!")
    for fmt, path in results.items():
        print(f"  {fmt}: {path}")


if __name__ == "__main__":
    main()
