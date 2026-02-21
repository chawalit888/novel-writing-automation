import { getBlogPostBySlug, getAllBlogPosts } from "@/lib/blog";
import { notFound } from "next/navigation";
import Link from "next/link";
import type { Metadata } from "next";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const posts = getAllBlogPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);
  if (!post) return {};

  return {
    title: post.title,
    description: post.excerpt,
    keywords: post.tags,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      locale: "th_TH",
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
    },
  };
}

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);
  if (!post) notFound();

  return (
    <article className="max-w-3xl mx-auto px-4 py-12">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-zinc-500 mb-8">
        <Link href="/" className="hover:text-amber-400 transition-colors">
          หน้าแรก
        </Link>
        <span>/</span>
        <Link href="/blog" className="hover:text-amber-400 transition-colors">
          บทความ
        </Link>
        <span>/</span>
        <span className="text-zinc-300 truncate">{post.title}</span>
      </nav>

      {/* Header */}
      <header className="mb-10">
        <h1 className="text-3xl md:text-4xl font-bold text-amber-50 mb-4">
          {post.title}
        </h1>
        <div className="flex items-center gap-3 text-sm">
          <span className="text-zinc-500">{post.publishedAt}</span>
          <div className="flex gap-2">
            {post.tags.map((tag) => (
              <span
                key={tag}
                className="text-amber-600 text-xs bg-amber-900/20 px-2 py-0.5 rounded"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="text-zinc-300 leading-relaxed space-y-4">
        {post.content.split("\n\n").map((block, i) => {
          if (block.startsWith("## ")) {
            return (
              <h2
                key={i}
                className="text-2xl font-bold text-amber-100 mt-8 mb-4"
              >
                {block.replace("## ", "")}
              </h2>
            );
          }
          if (block.startsWith("### ")) {
            return (
              <h3
                key={i}
                className="text-xl font-semibold text-amber-200 mt-6 mb-3"
              >
                {block.replace("### ", "")}
              </h3>
            );
          }
          if (block.startsWith("- ")) {
            const items = block.split("\n");
            return (
              <ul key={i} className="space-y-2 ml-4">
                {items.map((item, j) => (
                  <li key={j} className="flex items-start gap-2">
                    <span className="text-amber-500 mt-1 shrink-0">
                      &bull;
                    </span>
                    <span
                      dangerouslySetInnerHTML={{
                        __html: item
                          .replace("- ", "")
                          .replace(
                            /\*\*(.*?)\*\*/g,
                            '<strong class="text-amber-200">$1</strong>'
                          ),
                      }}
                    />
                  </li>
                ))}
              </ul>
            );
          }
          return <p key={i}>{block}</p>;
        })}
      </div>

      {/* Back */}
      <div className="mt-12 pt-8 border-t border-zinc-800">
        <Link
          href="/blog"
          className="text-amber-500 hover:text-amber-400 transition-colors"
        >
          &larr; กลับไปบทความทั้งหมด
        </Link>
      </div>
    </article>
  );
}
