import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'EHB AI Dev Studio - Your AI Development Partner',
  description: 'Build applications with AI assistance. No coding required.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
          {children}
        </div>
      </body>
    </html>
  )
}
