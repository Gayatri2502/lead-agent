import type { Metadata, Viewport } from 'next';
import { Providers } from './providers';
import '@/styles/globals.css';

export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
};

export const metadata: Metadata = {
  title: {
    default: 'AI Voice Receptionist - Dashboard',
    template: '%s | AI Voice Receptionist',
  },
  description: 'Manage appointments, track calls, and analyze customer interactions with AI-powered insights.',
  keywords: ['AI receptionist', 'appointment booking', 'call management', 'customer management', 'business automation'],
  authors: [{ name: 'AI Voice Receptionist' }],
  creator: 'AI Voice Receptionist',
  publisher: 'AI Voice Receptionist',
  robots: {
    index: false,
    follow: false,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://voice-receptionist.app',
    siteName: 'AI Voice Receptionist',
    title: 'AI Voice Receptionist - Dashboard',
    description: 'Manage appointments, track calls, and analyze customer interactions with AI-powered insights.',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'AI Voice Receptionist Dashboard',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI Voice Receptionist - Dashboard',
    description: 'Manage appointments, track calls, and analyze customer interactions with AI-powered insights.',
    images: ['/og-image.png'],
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="bg-background text-foreground antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}