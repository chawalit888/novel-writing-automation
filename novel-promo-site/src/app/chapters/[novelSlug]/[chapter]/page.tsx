import { getNovelBySlug, getChapter, getChaptersForNovel } from "@/lib/novels";
import { notFound } from "next/navigation";
import Link from "next/link";
import type { Metadata } from "next";
import PlatformLinks from "@/components/PlatformLinks";

interface Props {
  params: Promise<{ novelSlug: string; chapter: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { novelSlug, chapter } = await params;
  const novel = getNovelBySlug(novelSlug);
  const chapterData = getChapter(novelSlug, chapter);
  if (!novel || !chapterData) return {};

  return {
    title: `${chapterData.title} - ${novel.title}`,
    description: `อ่าน${chapterData.title}ของนิยาย ${novel.title} (${novel.titleEn}) ฟรี`,
    openGraph: {
      title: `${chapterData.title} - ${novel.title}`,
      description: `อ่าน${chapterData.title}ของนิยาย ${novel.title} ฟรี`,
      type: "article",
      locale: "th_TH",
    },
  };
}

export default async function ChapterPage({ params }: Props) {
  const { novelSlug, chapter } = await params;
  const novel = getNovelBySlug(novelSlug);
  const chapterData = getChapter(novelSlug, chapter);

  if (!novel || !chapterData) notFound();

  const allChapters = getChaptersForNovel(novelSlug).filter((ch) => ch.isFree);
  const currentIdx = allChapters.findIndex((ch) => ch.slug === chapter);
  const prevChapter = currentIdx > 0 ? allChapters[currentIdx - 1] : null;
  const nextChapter =
    currentIdx < allChapters.length - 1 ? allChapters[currentIdx + 1] : null;

  return (
    <article className="max-w-3xl mx-auto px-4 py-12">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-zinc-500 mb-8">
        <Link href="/" className="hover:text-amber-400 transition-colors">
          หน้าแรก
        </Link>
        <span>/</span>
        <Link
          href={`/novels/${novelSlug}`}
          className="hover:text-amber-400 transition-colors"
        >
          {novel.title}
        </Link>
        <span>/</span>
        <span className="text-zinc-300">{chapterData.title}</span>
      </nav>

      {/* Chapter header */}
      <header className="mb-10">
        <p className="text-amber-500 text-sm font-semibold mb-2">
          {novel.title}
        </p>
        <h1 className="text-3xl font-bold text-amber-50 mb-4">
          {chapterData.title}
        </h1>
        {chapterData.isFree && (
          <span className="bg-green-900/50 text-green-400 text-xs px-3 py-1 rounded-full">
            ตอนฟรี
          </span>
        )}
      </header>

      {/* Content */}
      <div className="text-zinc-300 leading-loose text-lg space-y-6">
        {chapterData.content.split("\n\n").map((paragraph, i) => (
          <p key={i}>{paragraph}</p>
        ))}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-12 pt-8 border-t border-zinc-800">
        {prevChapter ? (
          <Link
            href={`/chapters/${novelSlug}/${prevChapter.slug}`}
            className="text-amber-500 hover:text-amber-400 transition-colors"
          >
            &larr; {prevChapter.title}
          </Link>
        ) : (
          <div />
        )}
        {nextChapter ? (
          <Link
            href={`/chapters/${novelSlug}/${nextChapter.slug}`}
            className="text-amber-500 hover:text-amber-400 transition-colors"
          >
            {nextChapter.title} &rarr;
          </Link>
        ) : (
          <Link
            href={`/novels/${novelSlug}`}
            className="text-amber-500 hover:text-amber-400 transition-colors"
          >
            กลับหน้านิยาย &rarr;
          </Link>
        )}
      </div>

      {/* CTA */}
      <div className="mt-12 bg-zinc-900 border border-zinc-800 rounded-xl p-6 text-center">
        <h3 className="text-amber-100 font-bold text-lg mb-2">
          ชอบเรื่องนี้ไหม?
        </h3>
        <div className="mt-4">
          <PlatformLinks
            platformUrls={novel.platformUrls}
            platforms={novel.platforms}
            primaryPlatform={novel.primaryPlatform}
            platform={novel.platform}
            platformUrl={novel.platformUrl}
          />
        </div>
      </div>
    </article>
  );
}
