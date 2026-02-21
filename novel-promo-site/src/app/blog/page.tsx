import { getAllBlogPosts } from "@/lib/blog";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "บทความ - แนะนำนิยาย Dark Romance และนิยายน่าอ่าน",
  description:
    "บทความแนะนำนิยายออนไลน์ Dark Romance, นิยายรัก NC, รีวิวนิยาย และเทคนิคการเขียนนิยาย",
};

export default function BlogPage() {
  const posts = getAllBlogPosts();

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-amber-100 mb-2">บทความ</h1>
      <p className="text-zinc-400 mb-10">
        แนะนำนิยาย รีวิว และบทความที่น่าสนใจ
      </p>

      {posts.length === 0 ? (
        <p className="text-zinc-500">ยังไม่มีบทความ - เร็วๆ นี้</p>
      ) : (
        <div className="space-y-6">
          {posts.map((post) => (
            <Link
              key={post.slug}
              href={`/blog/${post.slug}`}
              className="group block bg-zinc-900 border border-zinc-800 rounded-xl p-6 hover:border-amber-700/50 transition-all"
            >
              <h2 className="text-xl font-bold text-amber-100 mb-2 group-hover:text-amber-400 transition-colors">
                {post.title}
              </h2>
              <p className="text-zinc-400 text-sm leading-relaxed mb-3">
                {post.excerpt}
              </p>
              <div className="flex items-center gap-3">
                <span className="text-zinc-600 text-xs">
                  {post.publishedAt}
                </span>
                <div className="flex gap-2">
                  {post.tags.slice(0, 3).map((tag) => (
                    <span
                      key={tag}
                      className="text-amber-600 text-xs bg-amber-900/20 px-2 py-0.5 rounded"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
