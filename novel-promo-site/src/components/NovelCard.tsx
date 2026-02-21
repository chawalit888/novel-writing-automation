import Link from "next/link";
import Image from "next/image";
import type { Novel } from "@/lib/novels";

const genreGradients: Record<string, string> = {
  "Dark Romance": "from-rose-900/80 via-purple-900/60 to-slate-900",
  "Mafia Romance": "from-red-950/80 via-zinc-900/60 to-slate-900",
  "CEO Romance": "from-amber-950/60 via-slate-900/60 to-indigo-950/40",
  "Office Romance": "from-blue-950/60 via-slate-900/60 to-purple-950/40",
  "Bodyguard Romance": "from-emerald-950/60 via-slate-900/60 to-cyan-950/40",
  Romance: "from-pink-950/60 via-slate-900/60 to-rose-950/40",
  default: "from-purple-950/60 via-slate-900/60 to-rose-950/40",
};

function getGradient(genres: string[]): string {
  for (const g of genres) {
    if (genreGradients[g]) return genreGradients[g];
  }
  return genreGradients.default;
}

export default function NovelCard({ novel }: { novel: Novel }) {
  const gradient = getGradient(novel.genre);

  return (
    <Link href={`/novels/${novel.slug}`} className="group block novel-card">
      <div className="relative rounded-2xl overflow-hidden border border-white/5 hover:border-rose-500/20">
        {/* Cover Image */}
        <div className="aspect-square relative bg-slate-900 overflow-hidden">
          {novel.coverImage ? (
            <>
              <Image
                src={novel.coverImage}
                alt={`ปกนิยาย ${novel.title}`}
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-500"
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              />
              {/* Dark overlay on hover */}
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300" />
            </>
          ) : (
            /* Fallback gradient if no image */
            <div className={`absolute inset-0 bg-gradient-to-br ${gradient} flex items-center justify-center`}>
              <div className="w-14 h-14 rounded-xl bg-white/10 backdrop-blur-sm flex items-center justify-center">
                <svg className="w-7 h-7 text-white/80" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                </svg>
              </div>
            </div>
          )}

          {/* Rating badge */}
          <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-rose-500/90 text-white text-xs font-bold shadow-lg shadow-rose-500/30">
            {novel.rating}
          </div>

          {/* Genre tags at bottom */}
          <div className="absolute bottom-3 left-3 flex gap-1.5 flex-wrap">
            {novel.genre.slice(0, 2).map((g) => (
              <span
                key={g}
                className="bg-black/40 backdrop-blur-sm text-white/70 text-xs px-2.5 py-0.5 rounded-full border border-white/10"
              >
                {g}
              </span>
            ))}
          </div>
        </div>

        {/* Info section */}
        <div className="p-4 bg-[#12121e]">
          {/* Title */}
          <h3 className="text-xl font-bold text-white mb-2 leading-tight line-clamp-2">
            {novel.title}
          </h3>
          {novel.titleEn && (
            <p className="text-xs text-white/40 mb-2">{novel.titleEn}</p>
          )}

          <p className="text-white/50 text-sm line-clamp-2 mb-3 leading-relaxed">
            {novel.logline}
          </p>
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-3 text-white/30">
              <span className="flex items-center gap-1">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                {novel.totalChapters} ตอน
              </span>
              <span className="flex items-center gap-1">
                <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                {novel.intensity}/10
              </span>
            </div>
            <span className="text-rose-400/60 font-medium">{novel.platform}</span>
          </div>
        </div>
      </div>
    </Link>
  );
}
