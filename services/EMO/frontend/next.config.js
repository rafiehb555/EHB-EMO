/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000',
    NEXT_PUBLIC_ADMIN_URL: process.env.NEXT_PUBLIC_ADMIN_URL || 'http://localhost:6001',
    NEXT_PUBLIC_AI_URL: process.env.NEXT_PUBLIC_AI_URL || 'http://localhost:5001',
    NEXT_PUBLIC_BLOCKCHAIN_URL: process.env.NEXT_PUBLIC_BLOCKCHAIN_URL || 'http://localhost:5002',
  },
  images: {
    domains: ['localhost', 'emo-business.com', 'api.emo-business.com'],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
      {
        source: '/ai/:path*',
        destination: `${process.env.NEXT_PUBLIC_AI_URL}/api/ai/:path*`,
      },
      {
        source: '/blockchain/:path*',
        destination: `${process.env.NEXT_PUBLIC_BLOCKCHAIN_URL}/api/blockchain/:path*`,
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig; 