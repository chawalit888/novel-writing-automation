import fs from "fs";
import path from "path";

export interface Character {
  name: string;
  role: string;
  age: number;
  description: string;
  quote: string;
}

export interface Novel {
  slug: string;
  title: string;
  titleEn: string;
  subtitle: string;
  author: string;
  genre: string[];
  rating: string;
  intensity: number;
  totalChapters: number;
  freeChapters: number;

  // Multi-platform support (NEW)
  platforms?: string[]; // ["Tunwalai", "ReadAWrite", "Dek-D"]
  platformUrls?: {
    tunwalai?: string;
    readawrite?: string;
    dekd?: string;
    fictionlog?: string;
    ookbee?: string;
    meb?: string;
  };
  primaryPlatform?: string; // "tunwalai"

  // Legacy fields (kept for backward compatibility)
  platform: string;
  platformUrl: string;

  status: string;
  coverImage: string;
  logline: string;
  synopsis: string;
  characters: Character[];
  hooks: string[];
  tags: string[];
  publishedAt: string;
  updatedAt: string;
}

export interface Chapter {
  slug: string;
  novelSlug: string;
  number: number;
  title: string;
  content: string;
  isFree: boolean;
  publishedAt: string;
}

const NOVELS_DIR = path.join(process.cwd(), "src/content/novels");
const CHAPTERS_DIR = path.join(process.cwd(), "src/content/chapters");

export function getAllNovels(): Novel[] {
  const files = fs.readdirSync(NOVELS_DIR).filter((f) => f.endsWith(".json"));
  return files
    .map((file) => {
      const content = fs.readFileSync(path.join(NOVELS_DIR, file), "utf-8");
      return JSON.parse(content) as Novel;
    })
    .sort(
      (a, b) =>
        new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
    );
}

export function getNovelBySlug(slug: string): Novel | null {
  const filePath = path.join(NOVELS_DIR, `${slug}.json`);
  if (!fs.existsSync(filePath)) return null;
  const content = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(content) as Novel;
}

export function getChaptersForNovel(novelSlug: string): Chapter[] {
  const dir = path.join(CHAPTERS_DIR, novelSlug);
  if (!fs.existsSync(dir)) return [];
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));
  return files
    .map((file) => {
      const content = fs.readFileSync(path.join(dir, file), "utf-8");
      return JSON.parse(content) as Chapter;
    })
    .sort((a, b) => a.number - b.number);
}

export function getChapter(
  novelSlug: string,
  chapterSlug: string
): Chapter | null {
  const filePath = path.join(CHAPTERS_DIR, novelSlug, `${chapterSlug}.json`);
  if (!fs.existsSync(filePath)) return null;
  const content = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(content) as Chapter;
}
