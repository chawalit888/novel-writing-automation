import { getNovelBySlug, getAllNovels, getChaptersForNovel } from "@/lib/novels";
import { notFound } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import type { Metadata } from "next";
import PlatformLinks from "@/components/PlatformLinks";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const novels = getAllNovels();
  return novels.map((novel) => ({ slug: novel.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const novel = getNovelBySlug(slug);
  if (!novel) return {};

  return {
    title: `${novel.title} (${novel.titleEn}) - ${novel.genre.join(", ")}`,
    description: novel.logline,
    keywords: novel.tags,
    openGraph: {
      title: `${novel.title} - ${novel.titleEn}`,
      description: novel.logline,
      type: "article",
      locale: "th_TH",
    },
  };
}

export default async function NovelDetailPage({ params }: Props) {
  const { slug } = await params;
  const novel = getNovelBySlug(slug);
  if (!novel) notFound();

  const chapters = getChaptersForNovel(slug);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Book",
    name: novel.title,
    alternateName: novel.titleEn,
    description: novel.logline,
    genre: novel.genre,
    inLanguage: "th",
    author: { "@type": "Person", name: novel.author },
    numberOfPages: novel.totalChapters,
    contentRating: novel.rating,
    keywords: novel.tags.join(", "),
  };

  return (
    <article>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Hero Section */}
      <section className="relative min-h-[70vh] flex items-end overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-novel-pattern" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-rose-600/8 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-0 w-[300px] h-[300px] bg-purple-600/5 rounded-full blur-[80px]" />

        {/* Gradient overlay at bottom */}
        <div className="absolute bottom-0 left-0 right-0 h-1/2 bg-gradient-to-t from-[#0a0a14] via-[#0a0a14]/80 to-transparent" />

        <div className="relative z-10 max-w-5xl mx-auto px-4 pb-12 pt-32 w-full">
          {/* Breadcrumb */}
          <nav className="flex items-center gap-2 text-sm text-white/30 mb-8">
            <Link href="/" className="hover:text-white/50 transition-colors">หน้าแรก</Link>
            <span>/</span>
            <span className="text-white/50">{novel.title}</span>
          </nav>

          {/* Title First - Full Width */}
          <div className="mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-3 leading-tight">
              {novel.title}
            </h1>
            {novel.titleEn && (
              <p className="text-xl text-white/40">{novel.titleEn}</p>
            )}
          </div>

          {/* Content Grid: Cover + Info */}
          <div className="grid grid-cols-1 md:grid-cols-[300px_1fr] gap-8 md:gap-12 items-start">
            {/* Cover Image */}
            {novel.coverImage && (
              <div className="mx-auto md:mx-0 w-[250px] md:w-[300px]">
                <div className="relative aspect-square rounded-2xl overflow-hidden shadow-2xl shadow-rose-500/10 border border-white/10 group">
                  <Image
                    src={novel.coverImage}
                    alt={`ปกนิยาย ${novel.title}`}
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 250px, 300px"
                    priority
                  />
                </div>
              </div>
            )}

            {/* Info */}
            <div className="flex flex-col">
              {/* Tags row */}
              <div className="flex items-center gap-2 mb-6 flex-wrap">
                <span className="px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 text-xs font-bold border border-rose-500/20">
                  {novel.rating}
                </span>
                {novel.genre.map((g) => (
                  <span
                    key={g}
                    className="px-3 py-1 rounded-full bg-white/5 text-white/50 text-xs border border-white/5"
                  >
                    {g}
                  </span>
                ))}
                <span className="px-3 py-1 rounded-full bg-purple-500/10 text-purple-300/60 text-xs border border-purple-500/10">
                  {novel.status}
                </span>
              </div>

              {/* Subtitle */}
              {novel.subtitle && (
                <p className="text-rose-400/70 text-lg mb-6">{novel.subtitle}</p>
              )}

              {/* Logline */}
              <blockquote className="relative pl-6 mb-8">
                <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-gradient-to-b from-rose-500 to-purple-500 rounded-full" />
                <p className="text-white/60 text-lg italic leading-relaxed">
                  {novel.logline}
                </p>
              </blockquote>

              {/* Meta info */}
              <div className="flex items-center gap-6 flex-wrap">
                <InfoBadge
                  icon={<BookIcon />}
                  label={`${novel.totalChapters} ตอน`}
                />
                <InfoBadge
                  icon={<StarIcon />}
                  label={`${novel.freeChapters} ตอนฟรี`}
                />
                <InfoBadge
                  icon={<FireIcon />}
                  label={`ความเข้มข้น ${novel.intensity}/10`}
                />
                <InfoBadge
                  icon={<GlobeIcon />}
                  label={novel.platform}
                  highlight
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Synopsis */}
      <section className="max-w-5xl mx-auto px-4 py-16">
        <SectionTitle>เรื่องย่อ</SectionTitle>
        <div className="text-white/55 leading-loose space-y-4 max-w-3xl">
          {novel.synopsis
            .split(/\n\n\[องก์|🔥 ความเข้มข้น|Warning Tags/)[0]
            .split("\n\n")
            .filter(p => !p.startsWith('#') && p.trim())
            .map((paragraph, i) => (
              <p key={i}>{paragraph}</p>
            ))}
        </div>
      </section>

      {/* Characters */}
      <section className="relative py-16 px-4">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-purple-950/5 to-transparent" />
        <div className="relative max-w-5xl mx-auto">
          <SectionTitle>ตัวละครหลัก</SectionTitle>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {novel.characters.map((char) => (
              <div
                key={char.name}
                className="group glass rounded-2xl p-6 hover:border-rose-500/10 transition-all duration-300"
              >
                <div className="flex items-center gap-3 mb-4">
                  <span className="px-3 py-1 rounded-full bg-rose-500/10 text-rose-400 text-xs font-semibold">
                    {char.role}
                  </span>
                  <span className="text-white/25 text-sm">{char.age} ปี</span>
                </div>
                <h3 className="text-white font-bold text-lg mb-2 group-hover:text-rose-300 transition-colors">
                  {char.name}
                </h3>
                <p className="text-white/40 text-sm leading-relaxed mb-4">
                  {char.description}
                </p>
                <div className="relative pl-4">
                  <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-gradient-to-b from-rose-500/40 to-purple-500/20 rounded-full" />
                  <p className="text-white/50 italic text-sm">
                    &ldquo;{char.quote}&rdquo;
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Hooks / Highlights */}
      <section className="max-w-5xl mx-auto px-4 py-16">
        <SectionTitle>คำโปรย</SectionTitle>
        <div className="space-y-4 max-w-3xl">
          {(() => {
            // Extract hooks from synopsis
            const hooksMatch = novel.synopsis.match(/คำโปรย\n\n([\s\S]*?)(?=Warning Tags|$)/);
            if (!hooksMatch) return null;

            const hooksText = hooksMatch[1];
            const quotes = hooksText.split(/💬/).filter(q => q.trim());

            return quotes.map((quote, i) => {
              const lines = quote.trim().split('\n').filter(l => l.trim());
              return (
                <div
                  key={i}
                  className="p-6 rounded-xl bg-gradient-to-br from-rose-500/5 to-purple-500/5 border border-white/5 hover:border-rose-500/10 transition-colors"
                >
                  <p className="text-white/70 text-lg leading-relaxed mb-3 italic">
                    {lines[0]?.replace(/^[""]|[""]$/g, '')}
                  </p>
                  {lines[lines.length - 1]?.startsWith('—') && (
                    <p className="text-rose-400/60 text-sm">
                      {lines[lines.length - 1]}
                    </p>
                  )}
                </div>
              );
            });
          })()}
        </div>
      </section>

      {/* Free Chapters */}
      {chapters.length > 0 && (
        <section className="relative py-16 px-4">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-rose-950/5 to-transparent" />
          <div className="relative max-w-5xl mx-auto">
            <SectionTitle>อ่านตัวอย่างฟรี</SectionTitle>
            <div className="space-y-3 max-w-2xl">
              {chapters
                .filter((ch) => ch.isFree)
                .map((ch) => (
                  <Link
                    key={ch.slug}
                    href={`/chapters/${novel.slug}/${ch.slug}`}
                    className="group flex items-center justify-between p-4 rounded-xl glass hover:border-rose-500/20 transition-all"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-rose-500/10 flex items-center justify-center">
                        <BookIcon />
                      </div>
                      <span className="text-white/80 group-hover:text-rose-300 transition-colors">
                        {ch.title}
                      </span>
                    </div>
                    <span className="text-rose-400/60 text-sm group-hover:text-rose-400 transition-colors flex items-center gap-1">
                      อ่านฟรี
                      <svg className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </span>
                  </Link>
                ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="relative max-w-5xl mx-auto px-4 py-20">
        <div className="relative text-center glass rounded-3xl p-10 md:p-16 overflow-hidden">
          {/* Background glow */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[300px] h-[200px] bg-rose-600/10 rounded-full blur-[80px]" />

          <div className="relative">
            <PlatformLinks
              platformUrls={novel.platformUrls}
              platforms={novel.platforms}
              primaryPlatform={novel.primaryPlatform}
              platform={novel.platform}
              platformUrl={novel.platformUrl}
            />
          </div>
        </div>
      </section>

      {/* Tags for SEO */}
      <section className="max-w-5xl mx-auto px-4 pb-16">
        <div className="flex flex-wrap gap-2">
          {novel.tags.map((tag) => (
            <span
              key={tag}
              className="px-3 py-1 rounded-full text-xs bg-white/[0.03] text-white/25 border border-white/5"
            >
              #{tag}
            </span>
          ))}
        </div>
      </section>
    </article>
  );
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-3 mb-8">
      <div className="w-1 h-6 bg-gradient-to-b from-rose-500 to-purple-500 rounded-full" />
      <h2 className="text-2xl font-bold text-white">{children}</h2>
    </div>
  );
}

function InfoBadge({ icon, label, highlight }: { icon: React.ReactNode; label: string; highlight?: boolean }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      <span className={highlight ? "text-rose-400" : "text-white/30"}>{icon}</span>
      <span className={highlight ? "text-rose-400 font-medium" : "text-white/40"}>{label}</span>
    </div>
  );
}

function BookIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
    </svg>
  );
}

function StarIcon() {
  return (
    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  );
}

function FireIcon() {
  return (
    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
    </svg>
  );
}

function GlobeIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
    </svg>
  );
}
