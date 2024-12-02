/** @type {import('next').NextConfig} */
const remotePatternsDev = [
  {
    hostname: process.env.NEXT_PUBLIC_GATEWAY_URL_NO_PORT_NO_HTTP_DEV,
  },
  {
    hostname: "localhost",
  }
]
const remotePatternsProd = [
  {
    hostname: process.env.NEXT_PUBLIC_GATEWAY_URL_NO_PORT_NO_HTTP,
  },
  {
    hostname: "localhost",
  }
]

const nextConfig = {
  images: {
    remotePatterns: process.env.NODE_ENV == "production" ? remotePatternsProd : remotePatternsDev
  },
  output: "standalone"
};

export default nextConfig;
