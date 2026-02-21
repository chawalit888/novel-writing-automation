#!/usr/bin/env python3
"""
Setup Project Script for n8n Novel System
สร้างโปรเจคนิยายใหม่พร้อมโครงสร้างไฟล์และ database entry
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
import uuid


# Genre configurations
GENRE_CONFIGS = {
    "romantic-comedy": {
        "ai_model": "gemini",
        "backup_ai_model": "gpt-4o-mini",
        "words_per_chapter": {"min": 3000, "target": 4000, "max": 6000},
        "quality_threshold_approve": 70,
        "temperature": 0.7,
        "focus": ["dialogue", "chemistry", "humor"]
    },
    "fantasy": {
        "ai_model": "gpt-4o",
        "backup_ai_model": "claude-haiku",
        "words_per_chapter": {"min": 4000, "target": 5000, "max": 7000},
        "quality_threshold_approve": 75,
        "temperature": 0.6,
        "focus": ["world-building", "consistency", "power-system"]
    },
    "horror": {
        "ai_model": "claude-haiku",
        "backup_ai_model": "gpt-4o",
        "words_per_chapter": {"min": 3000, "target": 4000, "max": 5000},
        "quality_threshold_approve": 75,
        "temperature": 0.5,
        "focus": ["atmosphere", "tension", "pacing"]
    },
    "mystery": {
        "ai_model": "gpt-4o",
        "backup_ai_model": "claude-haiku",
        "words_per_chapter": {"min": 3500, "target": 4500, "max": 6000},
        "quality_threshold_approve": 80,
        "temperature": 0.4,
        "focus": ["logic", "clues", "timeline"]
    },
    "bl-gl": {
        "ai_model": "claude-haiku",
        "backup_ai_model": "gemini",
        "words_per_chapter": {"min": 3000, "target": 4000, "max": 5500},
        "quality_threshold_approve": 70,
        "temperature": 0.6,
        "focus": ["relationship", "emotion", "chemistry"]
    }
}


def generate_project_id(title: str, genre: str) -> str:
    """Generate unique project ID"""
    # Clean title for ID
    clean_title = "".join(c for c in title.lower() if c.isalnum() or c == ' ')
    clean_title = clean_title.replace(' ', '-')[:20]

    # Add genre prefix and short uuid
    short_uuid = str(uuid.uuid4())[:8]
    return f"{genre[:3]}-{clean_title}-{short_uuid}"


def create_project_structure(base_path: Path, project_id: str) -> Path:
    """Create directory structure for new project"""
    project_path = base_path / "stories" / project_id

    # Create directories
    directories = [
        project_path / "chapters",
    ]

    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)

    return project_path


def create_config_file(project_path: Path, config: Dict) -> Path:
    """Create config.json for the project"""
    config_path = project_path / "config.json"

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    return config_path


def create_characters_file(project_path: Path, num_characters: int = 3) -> Path:
    """Create placeholder characters.json"""
    characters = []

    for i in range(num_characters):
        characters.append({
            "id": f"char-{i+1:03d}",
            "name": f"Character {i+1}",
            "role": "protagonist" if i == 0 else "supporting",
            "age": 20 + i * 2,
            "personality": [],
            "background": "",
            "motivation": "",
            "to_be_generated": True
        })

    chars_path = project_path / "characters.json"
    with open(chars_path, 'w', encoding='utf-8') as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)

    return chars_path


def create_outline_file(project_path: Path, target_chapters: int) -> Path:
    """Create placeholder outline.txt"""
    outline = f"""# Master Outline

## Overview
[To be generated]

## Target: {target_chapters} chapters

## Chapter Outline

"""
    for i in range(1, target_chapters + 1):
        outline += f"\n### Chapter {i}\n[To be generated]\n"

    outline_path = project_path / "outline.txt"
    with open(outline_path, 'w', encoding='utf-8') as f:
        f.write(outline)

    return outline_path


def create_metadata_file(project_path: Path, config: Dict) -> Path:
    """Create metadata.json"""
    metadata = {
        "project_id": config['project_id'],
        "title": config['title'],
        "genre": config['genre'],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "setup",
        "current_chapter": 0,
        "total_words": 0,
        "characters_generated": False,
        "outline_generated": False,
        "last_activity": None
    }

    meta_path = project_path / "metadata.json"
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return meta_path


def setup_project(
    title: str,
    genre: str,
    target_chapters: int = 20,
    description: str = "",
    price_per_chapter: float = 30,
    base_path: Optional[str] = None
) -> Dict:
    """
    Setup a new novel project

    Args:
        title: Novel title
        genre: Genre (romantic-comedy, fantasy, horror, mystery, bl-gl)
        target_chapters: Target number of chapters
        description: Novel description
        price_per_chapter: Price per chapter (THB)
        base_path: Base path for n8n-novels directory

    Returns:
        Project configuration dictionary
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent
    else:
        base_path = Path(base_path)

    # Validate genre
    if genre not in GENRE_CONFIGS:
        available = ", ".join(GENRE_CONFIGS.keys())
        raise ValueError(f"Invalid genre: {genre}. Available: {available}")

    # Get genre config
    genre_config = GENRE_CONFIGS[genre]

    # Generate project ID
    project_id = generate_project_id(title, genre)

    # Create full config
    config = {
        "project_id": project_id,
        "title": title,
        "genre": genre,
        "ai_model": genre_config["ai_model"],
        "backup_ai_model": genre_config["backup_ai_model"],
        "target_chapters": target_chapters,
        "words_per_chapter": genre_config["words_per_chapter"],
        "quality_thresholds": {
            "auto_approve": genre_config["quality_threshold_approve"],
            "manual_review": genre_config["quality_threshold_approve"] - 5,
            "auto_regenerate": genre_config["quality_threshold_approve"] - 15
        },
        "schedule": {
            "frequency": "daily",
            "time": "09:00",
            "timezone": "Asia/Bangkok"
        },
        "price_per_chapter": price_per_chapter,
        "target_platform": ["ookbee", "meb"],
        "tags": [],
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "author": "AI Writer",
            "description": description,
            "cover_image": ""
        },
        "ai_settings": {
            "temperature": genre_config["temperature"],
            "focus": genre_config["focus"]
        }
    }

    # Create directory structure
    project_path = create_project_structure(base_path, project_id)

    # Create files
    create_config_file(project_path, config)
    create_characters_file(project_path)
    create_outline_file(project_path, target_chapters)
    create_metadata_file(project_path, config)

    print(f"\n{'='*60}")
    print(f" Project Created Successfully!")
    print(f"{'='*60}")
    print(f" Title:          {title}")
    print(f" Project ID:     {project_id}")
    print(f" Genre:          {genre}")
    print(f" AI Model:       {genre_config['ai_model']}")
    print(f" Target:         {target_chapters} chapters")
    print(f" Path:           {project_path}")
    print(f"{'='*60}")
    print(f"\nNext Steps:")
    print(f" 1. Run Character Generator workflow")
    print(f" 2. Run Plot Outliner workflow")
    print(f" 3. Start Daily Writer workflow")
    print(f"{'='*60}\n")

    return config


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Setup new novel project')
    parser.add_argument('title', help='Novel title')
    parser.add_argument('--genre', required=True,
                        choices=list(GENRE_CONFIGS.keys()),
                        help='Novel genre')
    parser.add_argument('--chapters', type=int, default=20,
                        help='Target number of chapters')
    parser.add_argument('--description', default='',
                        help='Novel description')
    parser.add_argument('--price', type=float, default=30,
                        help='Price per chapter (THB)')
    parser.add_argument('--base-path', help='Base path for n8n-novels')

    args = parser.parse_args()

    try:
        config = setup_project(
            title=args.title,
            genre=args.genre,
            target_chapters=args.chapters,
            description=args.description,
            price_per_chapter=args.price,
            base_path=args.base_path
        )
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
