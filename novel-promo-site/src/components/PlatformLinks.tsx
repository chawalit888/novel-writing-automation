import { PLATFORMS, PlatformKey } from "@/config/platforms";

interface PlatformLinksProps {
  platformUrls?: Record<string, string>;
  platforms?: string[];
  primaryPlatform?: string;
  // Legacy support
  platform?: string;
  platformUrl?: string;
}

export default function PlatformLinks({
  platformUrls,
  platforms,
  primaryPlatform,
  platform,
  platformUrl,
}: PlatformLinksProps) {
  // Check if we have new multi-platform data
  const hasMultiPlatform = platformUrls && Object.keys(platformUrls).length > 0;

  // Fallback to legacy single platform
  const hasLegacyPlatform = !hasMultiPlatform && platform && platformUrl;

  if (!hasMultiPlatform && !hasLegacyPlatform) {
    return (
      <p className="text-white/30 text-sm">(ลิงก์จะเพิ่มเมื่อเผยแพร่แล้ว)</p>
    );
  }

  // Render legacy single platform
  if (hasLegacyPlatform) {
    return (
      <a
        href={platformUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block px-6 py-3 rounded-lg bg-gradient-to-r from-pink-500 to-rose-500 text-white font-medium hover:from-pink-600 hover:to-rose-600 transition-all shadow-lg hover:shadow-xl"
      >
        อ่านบน {platform}
      </a>
    );
  }

  // Render multi-platform links
  const sortedPlatformKeys = Object.keys(platformUrls!)
    .filter((key) => platformUrls![key]) // Only show platforms with URLs
    .sort((a, b) => {
      // Primary platform first
      if (a === primaryPlatform) return -1;
      if (b === primaryPlatform) return 1;
      // Then alphabetically
      return a.localeCompare(b);
    }) as PlatformKey[];

  if (sortedPlatformKeys.length === 0) {
    return (
      <p className="text-white/30 text-sm">(ลิงก์จะเพิ่มเมื่อเผยแพร่แล้ว)</p>
    );
  }

  return (
    <div className="space-y-3">
      <h3 className="text-white/80 text-sm font-medium">อ่านเรื่องเต็มได้ที่:</h3>
      <div className="flex flex-wrap gap-3">
        {sortedPlatformKeys.map((key) => {
          const config = PLATFORMS[key];
          const url = platformUrls![key];

          if (!config || !url) return null;

          const isPrimary = key === primaryPlatform;

          return (
            <a
              key={key}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className={`
                inline-flex items-center gap-2 px-5 py-2.5 rounded-lg font-medium
                transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5
                ${isPrimary ? "ring-2 ring-white/30" : ""}
              `}
              style={{
                background: `linear-gradient(135deg, ${config.color}, ${config.color}dd)`,
                color: "white",
              }}
              title={`อ่านบน ${config.name}`}
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
              <span>{config.name}</span>
              {isPrimary && (
                <span className="text-xs bg-white/20 px-1.5 py-0.5 rounded">
                  หลัก
                </span>
              )}
            </a>
          );
        })}
      </div>
    </div>
  );
}
