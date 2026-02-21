#!/usr/bin/env python3
"""
Blog Post Generator using Gemini 1.5 Pro API (Free Tier)
Generates SEO-friendly Thai articles with images from Unsplash
"""

import os
import json
import re
import requests
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai import types
import time

# Configuration
BLOG_CONTENT_PLAN = Path(__file__).parent.parent / "blog-content-plan.json"
BLOG_OUTPUT_DIR = Path(__file__).parent.parent / "novel-promo-site/src/content/blog"
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def generate_slug(title):
    """Convert Thai title to URL-friendly slug (English only for Next.js compatibility)"""
    # Extract numbers from title
    numbers = re.findall(r'\d+', title)
    number_prefix = numbers[0] if numbers else ""

    # Transliteration mapping for common Thai words in titles
    thai_to_english = {
        'นิยาย': 'niyai',
        'รัก': 'rak',
        'nc': 'nc',
        'โรแมนติก': 'romantic',
        'น่าอ่าน': 'na-an',
        'ประจำปี': 'pracham-pi',
        'dark': 'dark',
        'romance': 'romance',
        'มาเฟีย': 'mafia',
        'อีโรติก': 'erotic',
        'สุด': 'sud',
        'เข้มข้น': 'khem-khon',
        'ห้าม': 'ham',
        'พลาด': 'phlad',
    }

    # Convert to lowercase
    slug = title.lower()

    # Replace Thai words with English
    for thai, english in thai_to_english.items():
        slug = slug.replace(thai, english)

    # Remove remaining Thai characters
    slug = re.sub(r'[\u0E00-\u0E7F]', '', slug)

    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)

    # Keep only English letters, numbers, and hyphens
    slug = re.sub(r'[^a-z0-9-]', '', slug)

    # Clean up multiple hyphens
    slug = re.sub(r'-+', '-', slug)

    # Add number prefix if exists
    if number_prefix and not slug.startswith(number_prefix):
        slug = f"{number_prefix}-{slug}"

    # Limit length
    slug = slug[:100]

    return slug.strip('-')

def get_local_novel_images(count=3):
    """Get novel cover images from local directory"""
    # Path to novel images directory
    novel_images_dir = Path(__file__).parent.parent / "novel-promo-site/public/images/novels"

    images = []

    if novel_images_dir.exists():
        # Get all novel subdirectories
        novel_dirs = [d for d in novel_images_dir.iterdir() if d.is_dir()]

        # Collect cover images from subdirectories
        for novel_dir in novel_dirs[:count]:
            # Look for cover image (cover.png, cover.jpg, cover.webp)
            cover_files = list(novel_dir.glob("cover.*"))

            if cover_files:
                cover_path = cover_files[0]
                images.append({
                    "url": f"/images/novels/{novel_dir.name}/{cover_path.name}",
                    "alt": f"Novel cover - {novel_dir.name}",
                    "photographer": None,
                    "photographer_url": None
                })

    # If no local images found, use placeholder URLs
    if not images:
        print("⚠️ No local images found, using placeholders")
        for i in range(count):
            images.append({
                "url": f"https://placehold.co/800x600/1a1a1a/white?text=Novel+{i+1}",
                "alt": f"Placeholder image {i+1}",
                "photographer": None,
                "photographer_url": None
            })

    return images

def download_unsplash_images(keywords, category, count=3):
    """Download images from Unsplash based on keywords and category"""
    if not UNSPLASH_ACCESS_KEY:
        print("⚠️ UNSPLASH_ACCESS_KEY not set, using local novel images instead")
        return get_local_novel_images(count)

    # Map Thai keywords to English for Unsplash search
    search_terms = {
        "educational": "books reading library elegant",
        "listicle": "bookshelf reading cozy aesthetic",
        "review": "book coffee reading romantic",
        "how-to": "writing notebook desk creative"
    }

    query = search_terms.get(category, "books reading")

    try:
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {
            "query": query,
            "per_page": count,
            "orientation": "landscape"
        }

        response = requests.get(
            "https://api.unsplash.com/search/photos",
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        images = []

        for photo in data.get("results", [])[:count]:
            images.append({
                "url": photo["urls"]["regular"],
                "alt": photo.get("alt_description", "Blog image"),
                "photographer": photo["user"]["name"],
                "photographer_url": photo["user"]["links"]["html"]
            })

        return images if images else get_local_novel_images(count)

    except Exception as e:
        print(f"⚠️ Error downloading Unsplash images: {e}")
        print("⚠️ Falling back to local novel images")
        return get_local_novel_images(count)

def generate_article(client, topic):
    """Generate blog article using Gemini 1.5 Pro"""
    prompt = f"""เขียนบทความภาษาไทยเกี่ยวกับหัวข้อ: {topic['title']}

คำสำคัญที่ต้องใช้: {', '.join(topic['keywords'])}
ประเภทบทความ: {topic['category']}
จำนวนคำเป้าหมาย: {topic['target_word_count']} คำ

เขียนบทความที่:
1. เป็นมิตรกับ SEO - ใช้คำสำคัญตามธรรมชาติ ไม่ยัดเยียด
2. มีโครงสร้างชัดเจน - มี H2, H3, bullet points, numbered lists
3. ให้ข้อมูลที่มีคุณค่า - ไม่ใช่แค่ SEO spam
4. ภาษาไทยเป็นธรรมชาติ เข้าใจง่าย
5. เหมาะกับผู้อ่านที่สนใจนิยาย NC, Dark Romance, อีโรติก
6. มีตัวอย่างเฉพาะเจาะจง (ชื่อเรื่อง, ชื่อแพลตฟอร์ม)

โครงสร้างบทความ:
- เริ่มต้นด้วยย่อหน้าแนะนำ (hook ที่น่าสนใจ)
- เนื้อหาหลัก 3-5 ส่วน (แต่ละส่วนมี H2 หรือ H3)
- สรุป + Call-to-Action

ห้าม:
- ใช้ emoji มากเกินไป
- เขียนแบบ clickbait หลอกลวง
- ใช้ข้อมูลที่ล้าสมัย
- คัดลอกเนื้อหาจากที่อื่น

เขียนเป็นรูปแบบ Markdown พร้อมใช้ ## สำหรับ H2 และ ### สำหรับ H3
"""

    try:
        print(f"🤖 Generating article: {topic['title']}")
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Faster, higher quota
            contents=prompt
        )

        if not response.text:
            raise Exception("Empty response from Gemini API")

        return response.text.strip()

    except Exception as e:
        print(f"❌ Error generating article: {e}")
        # Retry once after 2 seconds
        print("⏳ Retrying in 2 seconds...")
        time.sleep(2)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",  # Faster, higher quota
                contents=prompt
            )
            return response.text.strip()
        except Exception as retry_error:
            print(f"❌ Retry failed: {retry_error}")
            raise

def create_blog_post(topic, article_content, images):
    """Create JSON blog post file"""
    slug = generate_slug(topic['title'])
    filename = f"{slug}.json"
    filepath = BLOG_OUTPUT_DIR / filename

    # Ensure output directory exists
    BLOG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Extract excerpt (first 200 characters)
    excerpt = article_content[:200].replace('\n', ' ').strip() + "..."

    # Add image credits to content if available (only for Unsplash images)
    content = article_content
    if images and any(img.get('photographer') for img in images):
        content += "\n\n---\n\n"
        content += "## ที่มาของภาพประกอบ\n\n"
        for img in images:
            if img.get('photographer'):
                content += f"- Photo by [{img['photographer']}]({img['photographer_url']}) on [Unsplash](https://unsplash.com)\n"

    # Create blog post JSON matching existing format
    blog_post = {
        "slug": slug,
        "title": topic['title'],
        "excerpt": excerpt,
        "content": content,
        "coverImage": images[0]["url"] if images else "/images/blog/placeholder.jpg",
        "tags": topic['keywords'],
        "publishedAt": datetime.now().strftime("%Y-%m-%d"),
        "updatedAt": datetime.now().strftime("%Y-%m-%d")
    }

    # Write JSON file
    filepath.write_text(json.dumps(blog_post, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ Created: {filepath}")

    return str(filepath)

def update_content_plan(topic_id, status, filepath=None, error=None):
    """Update blog-content-plan.json with completion status"""
    with open(BLOG_CONTENT_PLAN, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    # Find and update topic
    for topic in plan['topics']:
        if topic['id'] == topic_id:
            topic['status'] = status
            topic['_updated_at'] = datetime.now().isoformat()

            if status == 'completed':
                topic['completed_at'] = datetime.now().isoformat()
                topic['file_path'] = filepath
                # Move to completed
                plan['completed'].append(topic)
                plan['topics'].remove(topic)
                # Update stats
                plan['stats']['completed'] += 1
                plan['stats']['pending'] = len([t for t in plan['topics'] if t['status'] == 'pending'])
            elif status == 'failed':
                topic['error'] = error
                topic['failed_at'] = datetime.now().isoformat()
                # Move to failed
                plan['failed'].append(topic)
                plan['topics'].remove(topic)
                # Update stats
                plan['stats']['failed'] += 1
                plan['stats']['pending'] = len([t for t in plan['topics'] if t['status'] == 'pending'])

            break

    # Save updated plan
    with open(BLOG_CONTENT_PLAN, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"📝 Updated content plan: {topic_id} -> {status}")

def main():
    """Main function - generate one blog post"""
    print("🚀 Blog Post Generator (Gemini 1.5 Pro)")
    print("=" * 50)

    # Check API keys
    if not GEMINI_API_KEY:
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("   Get your free API key: https://makersuite.google.com/app/apikey")
        return 1

    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Load content plan
    if not BLOG_CONTENT_PLAN.exists():
        print(f"❌ Error: Content plan not found: {BLOG_CONTENT_PLAN}")
        return 1

    with open(BLOG_CONTENT_PLAN, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    # Find first pending topic
    pending_topics = [t for t in plan['topics'] if t['status'] == 'pending']

    if not pending_topics:
        print("✅ No pending topics! All articles generated.")
        return 0

    # Get highest priority topic
    topic = min(pending_topics, key=lambda t: t.get('priority', 99))

    print(f"\n📰 Topic: {topic['title']}")
    print(f"📂 Category: {topic['category']}")
    print(f"🔑 Keywords: {', '.join(topic['keywords'])}")
    print(f"📊 Target words: {topic['target_word_count']}")
    print()

    try:
        # Download images first
        print("🖼️ Downloading images from Unsplash...")
        images = download_unsplash_images(
            topic['keywords'],
            topic['category'],
            count=3
        )
        print(f"✅ Downloaded {len(images)} images")

        # Generate article
        article = generate_article(client, topic)
        word_count = len(article.split())
        print(f"✅ Generated article: {word_count} words")

        # Create blog post file
        filepath = create_blog_post(topic, article, images)

        # Update content plan
        update_content_plan(topic['id'], 'completed', filepath)

        print()
        print("=" * 50)
        print("✅ SUCCESS!")
        print(f"📄 Article: {filepath}")
        print(f"📊 Stats: {plan['stats']['completed'] + 1}/{len(plan['topics']) + len(plan['completed'])} completed")
        print("=" * 50)

        return 0

    except Exception as e:
        print()
        print("=" * 50)
        print(f"❌ FAILED: {e}")
        print("=" * 50)

        # Update content plan with error
        update_content_plan(topic['id'], 'failed', error=str(e))

        return 1

if __name__ == "__main__":
    exit(main())
