import type { Metadata } from "next";
import Script from "next/script";
import { Noto_Sans_Thai } from "next/font/google";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import "./globals.css";

const GA_ID = process.env.NEXT_PUBLIC_GA_ID;

const notoThai = Noto_Sans_Thai({
  variable: "--font-noto-thai",
  subsets: ["thai", "latin"],
  weight: ["300", "400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: {
    default: "NC Story - นิยายออนไลน์ Dark Romance สุดเข้มข้น",
    template: "%s | NC Story",
  },
  description:
    "อ่านนิยายออนไลน์ Dark Romance, นิยายรัก NC สุดเข้มข้น ตัวอย่างฟรี พร้อมบทความแนะนำนิยายน่าอ่าน",
  keywords: [
    "นิยายออนไลน์",
    "นิยายอิโรติก",
    "นิยายอีโรติก",
    "อิโรติก",
    "อีโรติก",
    "นิยายรักอิโรติก",
    "นิยายอีโรติค",
    "อีโรติค",
    "นิยายโรแมนติก",
    "อ่านนิยายอีโรติคฟรี",
    "นิยายnc30",
    "อิโรติกนิยาย",
    "อ่านนิยายอีโรติก",
    "นิยายอิโรติก20",
    "อิโรติค",
    "อิโรติกเกาหลี",
    "อีโรติคเกาหลี",
    "อ่านนิยายฟรีจบเล่ม",
    "เรื่องเล่าอิโรติก",
    "อ่านนิยายฟรี",
    "อ่านนิยายรัก",
    "นิยายผู้ใหญ่",
    "อ่านนิยายออนไลน์ฟรี",
    "อ่านนิยายออนไลน์",
    "อ่านนิยาย",
    "นิยาย",
    "นวนิยาย",
    "นิยายncมาเฟีย",
    "นิยาย25",
    "นิยายncฟรี",
    "นิยายnc",
    "Dark Romance",
    "นิยายรัก",
    "Tunwalai",
    "นิยายไทย",
    "NC Story",
    "คุณหนูจอมหื่น",
  ],
  authors: [{ name: "คุณหนูจอมหื่น" }],
  openGraph: {
    type: "website",
    locale: "th_TH",
    siteName: "NC Story",
    title: "NC Story - นิยายออนไลน์ Dark Romance สุดเข้มข้น",
    description:
      "อ่านนิยายออนไลน์ Dark Romance, นิยายรัก NC สุดเข้มข้น ตัวอย่างฟรี",
  },
  twitter: {
    card: "summary_large_image",
    title: "NC Story - นิยายออนไลน์ Dark Romance สุดเข้มข้น",
    description:
      "อ่านนิยายออนไลน์ Dark Romance, นิยายรัก NC สุดเข้มข้น ตัวอย่างฟรี",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="th">
      <head>
        {/* JSON-LD Structured Data */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              name: "NC Story",
              description:
                "อ่านนิยายออนไลน์ Dark Romance, นิยายรัก NC สุดเข้มข้น",
              url: "https://nc-story.com",
              inLanguage: "th",
              author: {
                "@type": "Person",
                name: "คุณหนูจอมหื่น",
              },
              publisher: {
                "@type": "Organization",
                name: "NC Story",
              },
            }),
          }}
        />
      </head>
      <body className={`${notoThai.variable} font-sans antialiased`}>
        {/* Google Analytics */}
        {GA_ID && (
          <>
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
              strategy="afterInteractive"
            />
            <Script id="google-analytics" strategy="afterInteractive">
              {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${GA_ID}');`}
            </Script>
          </>
        )}
        <Header />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
