import Link from "next/link";

export default function Footer() {
  return (
    <footer className="relative border-t border-white/5">
      {/* Gradient top line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-rose-500/30 to-transparent" />

      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-rose-500 to-purple-600 flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                </svg>
              </div>
              <span className="font-bold text-lg">
                <span className="text-gradient-rose">NC</span>
                <span className="text-white/90"> Story</span>
              </span>
            </div>
            <p className="text-white/40 text-sm leading-relaxed max-w-xs">
              เว็บไซต์รวมนิยายออนไลน์โดย <span className="text-rose-400/80">คุณหนูจอมหื่น</span> อ่านตัวอย่างฟรี ติดตามนิยายรักโรแมนติก Dark Romance ที่คุณชื่นชอบ
            </p>
          </div>

          {/* Quick links */}
          <div>
            <h4 className="text-white/80 font-semibold mb-4 text-sm tracking-wide uppercase">
              ลิงก์ด่วน
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link href="/" className="text-white/40 hover:text-rose-400 transition-colors">
                  หน้าแรก
                </Link>
              </li>
              <li>
                <Link href="/blog" className="text-white/40 hover:text-rose-400 transition-colors">
                  บทความ
                </Link>
              </li>
            </ul>
          </div>

          {/* Platform */}
          <div>
            <h4 className="text-white/80 font-semibold mb-4 text-sm tracking-wide uppercase">
              แพลตฟอร์ม
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <span className="text-white/40">Tunwalai</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-10 pt-6 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-white/25 text-xs">
            &copy; {new Date().getFullYear()} NC Story by คุณหนูจอมหื่น. All rights reserved.
          </p>
          <p className="text-white/20 text-xs">
            เขียนด้วยรักสำหรับผู้อ่านนิยาย
          </p>
        </div>
      </div>
    </footer>
  );
}
