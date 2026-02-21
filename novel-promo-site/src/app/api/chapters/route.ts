import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { getChaptersForNovel } from "@/lib/novels";

const CHAPTERS_DIR = path.join(process.cwd(), "src/content/chapters");
const API_KEY = process.env.API_KEY || "your-secret-api-key";

function checkAuth(request: NextRequest): boolean {
  const authHeader = request.headers.get("authorization");
  return authHeader === `Bearer ${API_KEY}`;
}

// GET - List chapters for a novel (?novel=slug)
export async function GET(request: NextRequest) {
  const novelSlug = request.nextUrl.searchParams.get("novel");
  if (!novelSlug) {
    return NextResponse.json(
      { error: "novel query param required" },
      { status: 400 }
    );
  }

  const chapters = getChaptersForNovel(novelSlug);
  return NextResponse.json({ chapters, count: chapters.length });
}

// POST - Create a new chapter (for n8n auto-post)
export async function POST(request: NextRequest) {
  if (!checkAuth(request)) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();

    if (!body.novelSlug || !body.slug || !body.title || !body.content) {
      return NextResponse.json(
        { error: "novelSlug, slug, title, and content are required" },
        { status: 400 }
      );
    }

    const novelDir = path.join(CHAPTERS_DIR, body.novelSlug);
    if (!fs.existsSync(novelDir)) {
      fs.mkdirSync(novelDir, { recursive: true });
    }

    const filePath = path.join(novelDir, `${body.slug}.json`);
    const chapterData = {
      slug: body.slug,
      novelSlug: body.novelSlug,
      number: body.number || 1,
      title: body.title,
      content: body.content,
      isFree: body.isFree ?? true,
      publishedAt: body.publishedAt || new Date().toISOString().split("T")[0],
    };

    fs.writeFileSync(filePath, JSON.stringify(chapterData, null, 2), "utf-8");

    return NextResponse.json(
      { message: "Chapter created", slug: body.slug },
      { status: 201 }
    );
  } catch {
    return NextResponse.json(
      { error: "Invalid request body" },
      { status: 400 }
    );
  }
}
