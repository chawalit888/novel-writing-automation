import type { MetadataRoute } from "next";
import { getAllNovels, getChaptersForNovel } from "@/lib/novels";
import { getAllBlogPosts } from "@/lib/blog";

const BASE_URL = process.env.SITE_URL || "https://nc-story.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const novels = getAllNovels();
  const blogPosts = getAllBlogPosts();

  const novelPages = novels.map((novel) => ({
    url: `${BASE_URL}/novels/${novel.slug}`,
    lastModified: new Date(novel.updatedAt),
    changeFrequency: "weekly" as const,
    priority: 0.9,
  }));

  const chapterPages = novels.flatMap((novel) =>
    getChaptersForNovel(novel.slug)
      .filter((ch) => ch.isFree)
      .map((ch) => ({
        url: `${BASE_URL}/chapters/${novel.slug}/${ch.slug}`,
        lastModified: new Date(ch.publishedAt),
        changeFrequency: "monthly" as const,
        priority: 0.7,
      }))
  );

  const blogPages = blogPosts.map((post) => ({
    url: `${BASE_URL}/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: "weekly" as const,
    priority: 0.8,
  }));

  return [
    {
      url: BASE_URL,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },
    {
      url: `${BASE_URL}/blog`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.8,
    },
    ...novelPages,
    ...chapterPages,
    ...blogPages,
  ];
}
