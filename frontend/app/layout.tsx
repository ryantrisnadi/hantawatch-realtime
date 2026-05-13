import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'HantaWatch Real-Time',
  description: 'Educational hantavirus surveillance dashboard with live public feed ingestion.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
