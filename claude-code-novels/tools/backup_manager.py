#!/usr/bin/env python3
"""
Backup Manager Tool
สำรองข้อมูลโปรเจคนิยาย
"""

import os
import shutil
import tarfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class BackupInfo:
    """Information about a backup"""
    name: str
    path: str
    date: str
    size_mb: float
    chapters: int
    words: int


class BackupManager:
    """Manage project backups"""

    def __init__(self, project_path: str, backup_dir: Optional[str] = None):
        self.project_path = Path(project_path)

        if backup_dir:
            self.backup_dir = Path(backup_dir)
        else:
            self.backup_dir = self.project_path.parent / "backups" / self.project_path.name

        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, include_exports: bool = False) -> BackupInfo:
        """
        Create a backup of the project

        Args:
            include_exports: Whether to include exports folder

        Returns:
            BackupInfo object
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = self.backup_dir / f"{backup_name}.tar.gz"

        # Folders to backup
        folders_to_backup = [
            "chapters",
            "characters",
            "world",
            "outlines",
            "metadata",
        ]

        files_to_backup = [
            "PROJECT.md",
            "PROJECT_MASTER.md",
        ]

        if include_exports:
            folders_to_backup.append("exports")

        # Create tar.gz
        with tarfile.open(backup_path, "w:gz") as tar:
            for folder in folders_to_backup:
                folder_path = self.project_path / folder
                if folder_path.exists():
                    tar.add(folder_path, arcname=folder)

            for file in files_to_backup:
                file_path = self.project_path / file
                if file_path.exists():
                    tar.add(file_path, arcname=file)

        # Get backup info
        size_mb = backup_path.stat().st_size / (1024 * 1024)

        # Count chapters and words
        chapters = 0
        words = 0
        chapters_path = self.project_path / "chapters"
        if chapters_path.exists():
            for f in chapters_path.glob("*.txt"):
                chapters += 1
                with open(f, 'r', encoding='utf-8') as file:
                    words += len(file.read().split())

        info = BackupInfo(
            name=backup_name,
            path=str(backup_path),
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            size_mb=round(size_mb, 2),
            chapters=chapters,
            words=words
        )

        # Save backup info
        self._save_backup_record(info)

        print(f"Backup created: {backup_path}")
        print(f"Size: {info.size_mb} MB | Chapters: {chapters} | Words: {words:,}")

        return info

    def _save_backup_record(self, info: BackupInfo):
        """Save backup record to JSON"""
        records_file = self.backup_dir / "backup_records.json"

        records = []
        if records_file.exists():
            with open(records_file, 'r', encoding='utf-8') as f:
                records = json.load(f)

        records.append({
            "name": info.name,
            "path": info.path,
            "date": info.date,
            "size_mb": info.size_mb,
            "chapters": info.chapters,
            "words": info.words
        })

        with open(records_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def list_backups(self) -> List[BackupInfo]:
        """List all available backups"""
        records_file = self.backup_dir / "backup_records.json"

        if not records_file.exists():
            return []

        with open(records_file, 'r', encoding='utf-8') as f:
            records = json.load(f)

        backups = []
        for r in records:
            if Path(r['path']).exists():
                backups.append(BackupInfo(**r))

        return backups

    def restore_backup(self, backup_name: str, target_path: Optional[str] = None) -> bool:
        """
        Restore a backup

        Args:
            backup_name: Name of backup to restore
            target_path: Where to restore (default: original project path)

        Returns:
            True if successful
        """
        backup_path = self.backup_dir / f"{backup_name}.tar.gz"

        if not backup_path.exists():
            print(f"Backup not found: {backup_path}")
            return False

        if target_path:
            restore_path = Path(target_path)
        else:
            restore_path = self.project_path

        # Create restore directory
        restore_path.mkdir(parents=True, exist_ok=True)

        # Extract
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(restore_path)

        print(f"Backup restored to: {restore_path}")
        return True

    def cleanup_old_backups(self, keep_days: int = 30, keep_min: int = 5):
        """
        Remove old backups

        Args:
            keep_days: Keep backups from last N days
            keep_min: Keep at least this many backups
        """
        backups = self.list_backups()

        if len(backups) <= keep_min:
            print(f"Only {len(backups)} backups exist. Keeping all.")
            return

        cutoff_date = datetime.now() - timedelta(days=keep_days)

        # Sort by date (newest first)
        backups.sort(key=lambda x: x.date, reverse=True)

        # Always keep minimum number
        to_keep = backups[:keep_min]
        to_check = backups[keep_min:]

        removed = 0
        for backup in to_check:
            backup_date = datetime.strptime(backup.date, "%Y-%m-%d %H:%M:%S")
            if backup_date < cutoff_date:
                try:
                    Path(backup.path).unlink()
                    removed += 1
                    print(f"Removed old backup: {backup.name}")
                except Exception as e:
                    print(f"Error removing {backup.name}: {e}")

        if removed == 0:
            print("No old backups to remove.")
        else:
            print(f"Removed {removed} old backup(s).")

    def get_backup_stats(self) -> dict:
        """Get backup statistics"""
        backups = self.list_backups()

        if not backups:
            return {"total": 0, "total_size_mb": 0}

        total_size = sum(b.size_mb for b in backups)

        return {
            "total": len(backups),
            "total_size_mb": round(total_size, 2),
            "oldest": backups[0].date if backups else None,
            "newest": backups[-1].date if backups else None,
        }


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Manage project backups')
    parser.add_argument('project_path', help='Path to project directory')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create backup
    create_parser = subparsers.add_parser('create', help='Create a backup')
    create_parser.add_argument('--include-exports', action='store_true',
                               help='Include exports folder')

    # List backups
    subparsers.add_parser('list', help='List all backups')

    # Restore backup
    restore_parser = subparsers.add_parser('restore', help='Restore a backup')
    restore_parser.add_argument('backup_name', help='Name of backup to restore')
    restore_parser.add_argument('--target', help='Target path for restore')

    # Cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Remove old backups')
    cleanup_parser.add_argument('--keep-days', type=int, default=30,
                                help='Keep backups from last N days')
    cleanup_parser.add_argument('--keep-min', type=int, default=5,
                                help='Keep at least N backups')

    args = parser.parse_args()

    manager = BackupManager(args.project_path)

    if args.command == 'create':
        manager.create_backup(include_exports=args.include_exports)

    elif args.command == 'list':
        backups = manager.list_backups()
        if not backups:
            print("No backups found.")
        else:
            print(f"\nFound {len(backups)} backup(s):\n")
            for b in backups:
                print(f"  {b.name}")
                print(f"    Date: {b.date}")
                print(f"    Size: {b.size_mb} MB | Chapters: {b.chapters}")
                print()

    elif args.command == 'restore':
        manager.restore_backup(args.backup_name, args.target)

    elif args.command == 'cleanup':
        manager.cleanup_old_backups(args.keep_days, args.keep_min)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
