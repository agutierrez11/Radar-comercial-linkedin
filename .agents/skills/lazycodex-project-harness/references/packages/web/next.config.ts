import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  allowedDevOrigins: ["127.0.0.1", "::1"],
  turbopack: {
    root: __dirname,
  },
}

export default nextConfig
