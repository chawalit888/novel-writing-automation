import NovelCard from "@/components/NovelCard";
import { getAllNovels } from "@/lib/novels";
import { getAllBlogPosts } from "@/lib/blog";
import Link from "next/link";

export default function HomePage() {
  const novels = getAllNovels();
  const blogPosts = getAllBlogPosts().slice(0, 3);

  const featured = novels[0];

  // Get unique genres for filter display
  const allGenres = Array.from(new Set(novels.flatMap((n) => n.genre)));

  return (
    <>
      {/* Hero Section */}
      {featured && (
        <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
          {/* Background effects */}
          <div className="absolute inset-0 bg-novel-pattern" />
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-rose-600/5 rounded-full blur-[120px]" />
          <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-purple-600/5 rounded-full blur-[100px]" />

          {/* Decorative floating elements */}
          <div className="absolute top-20 left-10 w-2 h-2 bg-rose-400/20 rounded-full animate-float" />
          <div className="absolute top-40 right-20 w-1.5 h-1.5 bg-purple-400/20 rounded-full animate-float" style={{ animationDelay: "1s" }} />
          <div className="absolute bottom-32 left-1/4 w-1 h-1 bg-amber-400/20 rounded-full animate-float" style={{ animationDelay: "2s" }} />

          <div className="relative z-10 max-w-5xl mx-auto px-4 text-center py-24">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass mb-8 animate-fade-in-up">
              <span className="w-2 h-2 bg-rose-500 rounded-full animate-pulse" />
              <span className="text-white/60 text-sm">
                Dark Romance & Mafia Romance
              </span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
              <span className="text-white">นิยายรัก</span>
              <br />
              <span className="text-gradient-rose">สุดเข้มข้น</span>
            </h1>

            <p className="text-white/50 text-lg md:text-xl max-w-2xl mx-auto mb-4 leading-relaxed animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
              {featured.logline}
            </p>

            <p className="text-rose-400/60 text-sm mb-10 animate-fade-in-up" style={{ animationDelay: "0.25s" }}>
              {featured.title} ({featured.titleEn})
            </p>

            {/* CTA Buttons */}
            <div className="flex items-center justify-center gap-4 flex-wrap animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
              <Link
                href={`/novels/${featured.slug}`}
                className="group relative px-8 py-3.5 rounded-full bg-gradient-to-r from-rose-600 to-purple-600 text-white font-semibold shadow-xl shadow-rose-500/20 hover:shadow-rose-500/30 transition-all hover:scale-105"
              >
                <span className="relative z-10">อ่านรายละเอียด</span>
              </Link>
              <Link
                href={`/chapters/${featured.slug}/chapter-01`}
                className="px-8 py-3.5 rounded-full border border-white/10 text-white/70 hover:text-white hover:border-rose-500/30 hover:bg-white/5 transition-all"
              >
                อ่านตัวอย่างฟรี
              </Link>
            </div>

            {/* Genre pills */}
            <div className="flex items-center justify-center gap-2 mt-10 flex-wrap animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
              {featured.genre.map((g) => (
                <span
                  key={g}
                  className="px-3 py-1 rounded-full text-xs bg-white/5 text-white/40 border border-white/5"
                >
                  {g}
                </span>
              ))}
              <span className="px-3 py-1 rounded-full text-xs bg-rose-500/10 text-rose-400/70 border border-rose-500/10">
                {featured.rating}
              </span>
            </div>
          </div>

          {/* Bottom fade */}
          <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[#0a0a14] to-transparent" />
        </section>
      )}

      {/* Stats bar */}
      <section className="max-w-6xl mx-auto px-4 -mt-8 relative z-20 mb-16">
        <div className="glass rounded-2xl p-6 flex flex-wrap items-center justify-center gap-8 md:gap-16">
          <div className="text-center">
            <p className="text-2xl font-bold text-gradient-rose">{novels.length}</p>
            <p className="text-white/30 text-xs mt-1">เรื่อง</p>
          </div>
          <div className="w-px h-8 bg-white/10 hidden md:block" />
          <div className="text-center">
            <p className="text-2xl font-bold text-gradient-purple">{allGenres.length}</p>
            <p className="text-white/30 text-xs mt-1">แนวนิยาย</p>
          </div>
          <div className="w-px h-8 bg-white/10 hidden md:block" />
          <div className="text-center">
            <p className="text-2xl font-bold text-gradient-gold">
              {novels.reduce((sum, n) => sum + n.totalChapters, 0)}+
            </p>
            <p className="text-white/30 text-xs mt-1">ตอน</p>
          </div>
          <div className="w-px h-8 bg-white/10 hidden md:block" />
          <div className="text-center">
            <p className="text-2xl font-bold text-white/80">Tunwalai</p>
            <p className="text-white/30 text-xs mt-1">แพลตฟอร์ม</p>
          </div>
        </div>
      </section>

      {/* Genre Filter Labels */}
      <section className="max-w-6xl mx-auto px-4 mb-8">
        <div className="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-hide">
          <span className="px-4 py-2 rounded-full text-sm bg-gradient-to-r from-rose-600/20 to-purple-600/20 text-rose-300 border border-rose-500/20 whitespace-nowrap cursor-default">
            ทั้งหมด
          </span>
          {allGenres.slice(0, 6).map((genre) => (
            <span
              key={genre}
              className="px-4 py-2 rounded-full text-sm bg-white/5 text-white/40 border border-white/5 whitespace-nowrap cursor-default hover:bg-white/10 hover:text-white/60 transition-colors"
            >
              {genre}
            </span>
          ))}
        </div>
      </section>

      {/* All Novels */}
      <section className="max-w-6xl mx-auto px-4 pb-20">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-white mb-1">นิยายทั้งหมด</h2>
            <p className="text-white/30 text-sm">{novels.length} เรื่อง รอคุณอยู่</p>
          </div>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
          {novels.map((novel) => (
            <NovelCard key={novel.slug} novel={novel} />
          ))}
        </div>
      </section>

      {/* Featured Quote */}
      {featured && featured.characters.length > 0 && (
        <section className="relative py-20 px-4 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-purple-950/10 to-transparent" />
          <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-rose-600/5 rounded-full blur-[80px]" />

          <div className="relative max-w-3xl mx-auto text-center">
            {/* Decorative quote mark */}
            <div className="text-6xl text-rose-500/10 font-serif leading-none mb-4">&ldquo;</div>
            <blockquote className="text-2xl md:text-3xl text-white/80 font-light italic leading-relaxed mb-6">
              {featured.characters[0].quote}
            </blockquote>
            <div className="flex items-center justify-center gap-3">
              <div className="w-8 h-px bg-gradient-to-r from-transparent to-rose-500/30" />
              <p className="text-rose-400 font-semibold text-sm">
                {featured.characters[0].name}
              </p>
              <div className="w-8 h-px bg-gradient-to-l from-transparent to-rose-500/30" />
            </div>
            <p className="text-white/20 text-xs mt-2">{featured.title}</p>
          </div>
        </section>
      )}

      {/* Blog Posts */}
      {blogPosts.length > 0 && (
        <section className="max-w-6xl mx-auto px-4 py-20">
          <div className="flex items-center justify-between mb-10">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">บทความล่าสุด</h2>
              <p className="text-white/30 text-sm">เรื่องน่ารู้เกี่ยวกับนิยาย</p>
            </div>
            <Link
              href="/blog"
              className="text-rose-400 hover:text-rose-300 text-sm font-medium transition-colors group"
            >
              ดูทั้งหมด
              <span className="inline-block ml-1 group-hover:translate-x-1 transition-transform">&rarr;</span>
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {blogPosts.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="group relative rounded-2xl overflow-hidden border border-white/5 hover:border-rose-500/20 transition-all duration-300 novel-card"
              >
                {/* Top accent line */}
                <div className="h-0.5 bg-gradient-to-r from-rose-500/0 via-rose-500/50 to-purple-500/0 group-hover:via-rose-400 transition-colors" />

                <div className="p-6 bg-[#12121e]">
                  <div className="flex flex-wrap gap-2 mb-3">
                    {post.tags.slice(0, 2).map((tag) => (
                      <span key={tag} className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-white/30">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <h3 className="text-white/90 font-semibold mb-2 group-hover:text-rose-300 transition-colors leading-snug">
                    {post.title}
                  </h3>
                  <p className="text-white/35 text-sm line-clamp-3 leading-relaxed">
                    {post.excerpt}
                  </p>
                  <div className="flex items-center justify-between mt-4 pt-4 border-t border-white/5">
                    <p className="text-white/20 text-xs">{post.publishedAt}</p>
                    <span className="text-rose-400/50 text-xs group-hover:text-rose-400 transition-colors">
                      อ่านต่อ &rarr;
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Bottom CTA */}
      <section className="relative py-20 px-4">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-rose-950/5 to-transparent" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            พร้อมเริ่มอ่านหรือยัง?
          </h2>
          <p className="text-white/40 mb-8">
            เริ่มอ่านตัวอย่างฟรีของนิยายที่คุณชอบได้เลย
          </p>
          <Link
            href={`/novels/${featured?.slug || "pantanakan-rattikan"}`}
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full bg-gradient-to-r from-rose-600 to-purple-600 text-white font-semibold shadow-xl shadow-rose-500/20 hover:shadow-rose-500/30 transition-all hover:scale-105"
          >
            เริ่มอ่านเลย
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </section>
    </>
  );
}
