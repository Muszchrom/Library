/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        hostname: "static01.helion.com.pl"
      }
    ]
  }
};

export default nextConfig;
