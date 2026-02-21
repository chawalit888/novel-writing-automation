#!/usr/bin/env python3
"""
Backup All Script
สำรองข้อมูลทั้งหมดของระบบ n8n novels
"""

import os
import tarfile
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import subprocess


class SystemBackup:
    """Backup entire n8n novel system"""

    def __init__(self, base_path: str, backup_dir: str = None):
        self.base_path = Path(base_path)

        if backup_dir:
            self.backup_dir = Path(backup_dir)
        else:
            self.backup_dir = self.base_path.parent / "backups" / "n8n-system"

        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def backup_stories(self, output_path: Path) -> int:
        """Backup all stories"""
        stories_path = self.base_path / "stories"
        count = 0

        if not stories_path.exists():
            return count

        stories_backup = output_path / "stories"
        stories_backup.mkdir(exist_ok=True)

        for story_dir in stories_path.iterdir():
            if story_dir.is_dir():
                shutil.copytree(story_dir, stories_backup / story_dir.name)
                count += 1

        return count

    def backup_workflows(self, output_path: Path) -> int:
        """Backup n8n workflows"""
        workflows_path = self.base_path / "n8n-data" / "workflows"
        count = 0

        if not workflows_path.exists():
            return count

        workflows_backup = output_path / "workflows"
        workflows_backup.mkdir(exist_ok=True)

        for wf_file in workflows_path.glob("*.json"):
            shutil.copy(wf_file, workflows_backup)
            count += 1

        return count

    def backup_database(self, output_path: Path) -> bool:
        """Backup PostgreSQL database using docker"""
        try:
            db_backup = output_path / "database"
            db_backup.mkdir(exist_ok=True)

            # Dump database using docker exec
            dump_file = db_backup / "database_dump.sql"

            cmd = [
                "docker", "exec", "n8n-postgres",
                "pg_dump", "-U", "n8n", "n8n_novels"
            ]

            with open(dump_file, 'w') as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE)

            if result.returncode == 0:
                print("  ✅ Database backed up")
                return True
            else:
                print(f"  ⚠️ Database backup failed: {result.stderr.decode()}")
                return False

        except Exception as e:
            print(f"  ⚠️ Database backup error: {e}")
            return False

    def backup_config(self, output_path: Path):
        """Backup configuration files"""
        config_files = [
            "docker-compose.yml",
            ".env.example",  # Not .env for security
        ]

        config_backup = output_path / "config"
        config_backup.mkdir(exist_ok=True)

        for cf in config_files:
            cf_path = self.base_path / cf
            if cf_path.exists():
                shutil.copy(cf_path, config_backup)

    def backup_prompts(self, output_path: Path):
        """Backup prompt templates"""
        prompts_path = self.base_path / "prompts"

        if prompts_path.exists():
            shutil.copytree(prompts_path, output_path / "prompts")

    def backup_templates(self, output_path: Path):
        """Backup templates"""
        templates_path = self.base_path / "templates"

        if templates_path.exists():
            shutil.copytree(templates_path, output_path / "templates")

    def create_full_backup(self, include_database: bool = True) -> Path:
        """
        Create full system backup

        Args:
            include_database: Whether to backup PostgreSQL database

        Returns:
            Path to backup archive
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"n8n_backup_{timestamp}"

        # Create temporary directory for backup
        temp_backup = self.backup_dir / backup_name
        temp_backup.mkdir(exist_ok=True)

        print(f"\n🔄 Creating backup: {backup_name}")
        print("-" * 50)

        # Backup stories
        print("📚 Backing up stories...")
        story_count = self.backup_stories(temp_backup)
        print(f"  ✅ {story_count} stories backed up")

        # Backup workflows
        print("⚙️ Backing up workflows...")
        wf_count = self.backup_workflows(temp_backup)
        print(f"  ✅ {wf_count} workflows backed up")

        # Backup database
        if include_database:
            print("🗄️ Backing up database...")
            self.backup_database(temp_backup)

        # Backup config
        print("📝 Backing up configuration...")
        self.backup_config(temp_backup)
        print("  ✅ Config backed up")

        # Backup prompts and templates
        print("📋 Backing up prompts and templates...")
        self.backup_prompts(temp_backup)
        self.backup_templates(temp_backup)
        print("  ✅ Prompts and templates backed up")

        # Create backup info
        info = {
            "backup_name": backup_name,
            "created_at": datetime.now().isoformat(),
            "stories_count": story_count,
            "workflows_count": wf_count,
            "includes_database": include_database
        }

        with open(temp_backup / "backup_info.json", 'w') as f:
            json.dump(info, f, indent=2)

        # Create tar.gz archive
        archive_path = self.backup_dir / f"{backup_name}.tar.gz"
        print("🗜️ Compressing backup...")

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(temp_backup, arcname=backup_name)

        # Clean up temp directory
        shutil.rmtree(temp_backup)

        # Get size
        size_mb = archive_path.stat().st_size / (1024 * 1024)

        print("-" * 50)
        print(f"✅ Backup complete: {archive_path}")
        print(f"📦 Size: {size_mb:.2f} MB")

        return archive_path

    def list_backups(self):
        """List all available backups"""
        backups = []

        for f in self.backup_dir.glob("n8n_backup_*.tar.gz"):
            stat = f.stat()
            backups.append({
                "name": f.stem,
                "path": str(f),
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })

        return sorted(backups, key=lambda x: x['date'], reverse=True)

    def cleanup_old_backups(self, keep_days: int = 30, keep_min: int = 5):
        """Remove old backups"""
        backups = self.list_backups()

        if len(backups) <= keep_min:
            print(f"Only {len(backups)} backups. Keeping all.")
            return

        cutoff = datetime.now() - timedelta(days=keep_days)
        removed = 0

        for backup in backups[keep_min:]:
            backup_date = datetime.strptime(backup['date'], "%Y-%m-%d %H:%M:%S")
            if backup_date < cutoff:
                Path(backup['path']).unlink()
                removed += 1
                print(f"Removed: {backup['name']}")

        print(f"Cleanup complete. Removed {removed} old backup(s).")

    def restore_backup(self, backup_name: str, target_path: str = None):
        """Restore from backup"""
        if not backup_name.endswith('.tar.gz'):
            backup_name = f"{backup_name}.tar.gz"

        backup_path = self.backup_dir / backup_name

        if not backup_path.exists():
            print(f"Backup not found: {backup_path}")
            return False

        if target_path:
            restore_to = Path(target_path)
        else:
            restore_to = self.base_path

        print(f"Restoring {backup_name} to {restore_to}...")

        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(restore_to.parent)

        print("✅ Restore complete")
        return True


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Backup n8n novel system')
    parser.add_argument('--base-path', default=str(Path(__file__).parent.parent),
                        help='Base path for n8n-novels')
    parser.add_argument('--backup-dir', help='Backup directory')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create backup
    create_parser = subparsers.add_parser('create', help='Create backup')
    create_parser.add_argument('--no-database', action='store_true',
                               help='Skip database backup')

    # List backups
    subparsers.add_parser('list', help='List backups')

    # Cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup old backups')
    cleanup_parser.add_argument('--keep-days', type=int, default=30)
    cleanup_parser.add_argument('--keep-min', type=int, default=5)

    # Restore
    restore_parser = subparsers.add_parser('restore', help='Restore backup')
    restore_parser.add_argument('backup_name', help='Backup name to restore')
    restore_parser.add_argument('--target', help='Target path')

    args = parser.parse_args()

    backup = SystemBackup(args.base_path, args.backup_dir)

    if args.command == 'create':
        backup.create_full_backup(include_database=not args.no_database)

    elif args.command == 'list':
        backups = backup.list_backups()
        if not backups:
            print("No backups found.")
        else:
            print(f"\n{'='*60}")
            print(f" Available Backups ({len(backups)})")
            print(f"{'='*60}")
            for b in backups:
                print(f" {b['name']}")
                print(f"   Date: {b['date']} | Size: {b['size_mb']} MB")
            print()

    elif args.command == 'cleanup':
        backup.cleanup_old_backups(args.keep_days, args.keep_min)

    elif args.command == 'restore':
        backup.restore_backup(args.backup_name, args.target)

    else:
        # Default: create backup
        backup.create_full_backup()


if __name__ == "__main__":
    main()
