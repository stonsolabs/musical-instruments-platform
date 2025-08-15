import './globals.css'
import type { Metadata } from 'next'
import Header from '../components/Header'
import Footer from '../components/Footer'

export const metadata: Metadata = {
  title: 'MusicEurope - Compare Musical Instruments Across Europe',
  description: 'Find the best deals on musical instruments across Europe. Compare prices, read reviews, and discover your next instrument.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <Header />
        <main>
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}


