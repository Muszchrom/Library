/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        // hostname: "static01.helion.com.pl",
        // hostname: process.env.BACKEND_URL
        hostname: process.env.BACKEND_URL_NO_PORT_NO_HTTP,

      }
    ]
  }
};

export default nextConfig;
