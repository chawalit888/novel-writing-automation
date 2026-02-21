import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { getAllNovels } from "@/lib/novels";

const NOVELS_DIR = path.join(process.cwd(), "src/content/novels");
const API_KEY = process.env.API_KEY || "your-secret-api-key";

function checkAuth(request: NextRequest): boolean {
  const authHeader = request.headers.get("authorization");
  return authHeader === `Bearer ${API_KEY}`;
}

// GET - List all novels
export async function GET() {
  const novels = getAllNovels();
  return NextResponse.json({ novels, count: novels.length });
}

// POST - Create a new novel (for n8n auto-post)
export async function POST(request: NextRequest) {
  if (!checkAuth(request)) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();

    if (!body.slug || !body.title) {
      return NextResponse.json(
        { error: "slug and title are required" },
        { status: 400 }
      );
    }

    const filePath = path.join(NOVELS_DIR, `${body.slug}.json`);
    fs.writeFileSync(filePath, JSON.stringify(body, null, 2), "utf-8");

    return NextResponse.json(
      { message: "Novel created", slug: body.slug },
      { status: 201 }
    );
  } catch {
    return NextResponse.json(
      { error: "Invalid request body" },
      { status: 400 }
    );
  }
}
