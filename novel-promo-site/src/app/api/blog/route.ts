import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { getAllBlogPosts } from "@/lib/blog";

const BLOG_DIR = path.join(process.cwd(), "src/content/blog");
const API_KEY = process.env.API_KEY || "your-secret-api-key";

function checkAuth(request: NextRequest): boolean {
  const authHeader = request.headers.get("authorization");
  return authHeader === `Bearer ${API_KEY}`;
}

// GET - List all blog posts
export async function GET() {
  const posts = getAllBlogPosts();
  return NextResponse.json({ posts, count: posts.length });
}

// POST - Create a new blog post (for n8n auto-post)
export async function POST(request: NextRequest) {
  if (!checkAuth(request)) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();

    if (!body.slug || !body.title || !body.content) {
      return NextResponse.json(
        { error: "slug, title, and content are required" },
        { status: 400 }
      );
    }

    const filePath = path.join(BLOG_DIR, `${body.slug}.json`);
    const postData = {
      slug: body.slug,
      title: body.title,
      excerpt: body.excerpt || body.content.substring(0, 200),
      content: body.content,
      coverImage: body.coverImage || "",
      tags: body.tags || [],
      publishedAt:
        body.publishedAt || new Date().toISOString().split("T")[0],
      updatedAt: new Date().toISOString().split("T")[0],
    };

    fs.writeFileSync(filePath, JSON.stringify(postData, null, 2), "utf-8");

    return NextResponse.json(
      { message: "Blog post created", slug: body.slug },
      { status: 201 }
    );
  } catch {
    return NextResponse.json(
      { error: "Invalid request body" },
      { status: 400 }
    );
  }
}
