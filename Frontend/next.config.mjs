/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        hostname: process.env.BACKEND_URL_NO_PORT_NO_HTTP,
      },
      {
        hostname: process.env.GATEWAY_URL_NO_PORT_NO_HTTP,
      },
      {
        hostname: "localhost",
      }
    ]
  },
  output: "standalone"
};

export default nextConfig;
